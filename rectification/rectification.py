import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils import get_calibration
from epipolar_geometry import compute_fundamental_matrix, rectification_homography


def transformed_corners(H, width, height):
    """
    Transform the four image corner points using a homography H.

    Shapes:
    -------
    H.shape                   = (3, 3)
    corners_homo.shape        = (4, 3)   # (x, y, 1) for each corner
    warped_corners_homo.shape = (4, 3)   # (x', y', w') after transform
    warped_corners.shape      = (4, 2)   # (x'/w', y'/w')

    Purpose:
    --------
    Determine where the image corners land after applying H.
    This is later used to compute the bounding box for warping.
    
    Returns:
    --------
    warped_corners
    """
    
    corners_homo = np.array(
        [
            [0, 0, 1],
            [width - 1, 0, 1],
            [width - 1, height - 1, 1],
            [0, height - 1, 1],
        ],
        dtype=np.float32,
    )
    warped_corners_homo = (H @ corners_homo.T).T # ((3,3) * (4,3).T).T = (3,4).T = (4,3)
    warped_corners = (warped_corners_homo / warped_corners_homo[:, -1, np.newaxis])[:, :2]
    return warped_corners

def tight_warp(
    left_img, right_img,
    H_left, H_right,
    width, height,
    border_value=(1, 1, 1),
):
    left_corners = transformed_corners(H_left, width, height)
    right_corners = transformed_corners(H_right, width, height)

    # independent x bounds
    min_x_left = int(np.floor(left_corners[:, 0].min()))
    max_x_left = int(np.ceil(left_corners[:, 0].max()))

    min_x_right = int(np.floor(right_corners[:, 0].min()))
    max_x_right = int(np.ceil(right_corners[:, 0].max()))

    # shared y bounds, but use intersection to avoid extra border fill
    min_y = int(np.ceil(max(
        left_corners[:, 1].min(),
        right_corners[:, 1].min(),
    )))

    max_y = int(np.floor(min(
        left_corners[:, 1].max(),
        right_corners[:, 1].max(),
    )))

    left_width = max_x_left - min_x_left + 1
    right_width = max_x_right - min_x_right + 1
    shared_height = max_y - min_y + 1

    shift_left = np.array([
        [1, 0, -min_x_left],
        [0, 1, -min_y],
        [0, 0, 1],
    ], dtype=np.float64)

    shift_right = np.array([
        [1, 0, -min_x_right],
        [0, 1, -min_y],
        [0, 0, 1],
    ], dtype=np.float64)

    H_left_shifted = shift_left @ H_left
    H_right_shifted = shift_right @ H_right

    left_rectified = cv2.warpPerspective(
        left_img,
        H_left_shifted,
        (left_width, shared_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )

    right_rectified = cv2.warpPerspective(
        right_img,
        H_right_shifted,
        (right_width, shared_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )

    return left_rectified, right_rectified, H_left_shifted, H_right_shifted


def loop_zhang_shear(H, width, height):
    """
    Compute the Loop Zhang shear matrix to horizontal reduce distortion after stereo rectification.

    Reference:
    ----------
    Loop & Zhang, "Computing Rectifying Homographies for Stereo Vision",
    CVPR 1999
    https://dev.ipol.im/~morel/Dossier_MVA_2011_Cours_Transparents_Documents/2011_Cours7_Document2_Loop-Zhang-CVPR1999.pdf

    Idea:
    -----
    After rectification, epipolar lines are horizontal (y = constant), but the image
    can appear distorted (skewed, stretched, or non-orthogonal).

    We want to reduce this distortion WITHOUT breaking rectification.

    Constraint:
    -----------
    The vertical coordinate must remain unchanged:
        y' = y

    Therefore, the only allowed transformation is:
        x' = s_a * x + s_b * y
        y' = y

    This corresponds to a horizontal scaling (s_a) and horizontal shear (s_b).

    Approach:
    ---------
    1. Take midpoints of the image borders (top, right, bottom, left).
    2. Transform them using the current homography H.
    3. Construct direction vectors:
           x = right - left     (horizontal direction)
           y = bottom - top     (vertical direction)
    4. Choose s_a and s_b such that:
           - x and y become orthogonal (reduce skew)
           - overall scaling distortion is minimized
    5. This leads to a closed-form solution for s_a and s_b.

    Result:
    -------
    Returns a shear matrix S such that:
        S @ H produces a rectified image with reduced distortion,
        while preserving horizontal epipolar alignment.
    """
    
    top_homo =    H @ [(width - 1) / 2, 0, 1.0]
    right_homo =  H @ [width - 1, (height - 1) / 2, 1.0]
    bottom_homo = H @ [(width - 1) / 2, height - 1, 1.0]
    left_homo =   H @ [0, (height - 1) / 2, 1.0]

    top = (top_homo / top_homo[-1])[:2]
    right = (right_homo / right_homo[-1])[:2]
    bottom = (bottom_homo / bottom_homo[-1])[:2]
    left = (left_homo / left_homo[-1])[:2]

    x = right - left
    y = bottom - top

    x_u, x_v = x
    y_u, y_v = y


    denom = height * width * (x_u * y_v - x_v * y_u)

    if abs(denom) < 1e-12:
        return np.eye(3)

    s_a = (height * height * x_v * x_v + width * width * y_v * y_v) / denom
    s_b = -(height * height * x_u * x_v + width * width * y_u * y_v) / denom

    if s_a < 0:
        s_a = -s_a
        s_b = -s_b

    S = np.array(
        [
            [s_a, s_b, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )

    return S


def stereo_rectify_no_cv2(K1, K2, R1_c2w, R2_c2w, C1_world, C2_world):
    """
    K1, K2:
        camera intrinsics.
        Map camera coordinates -> image pixel coordinates.

    R1_c2w, R2_c2w:
        camera-to-world rotations.
        Map directions from camera coordinates -> world coordinates.

        Example:
            direction_world = R_c2w @ direction_camera

        Columns:
            R_c2w[:, 0] = camera x-axis in world coordinates
            R_c2w[:, 1] = camera y-axis in world coordinates
            R_c2w[:, 2] = camera z-axis in world coordinates

    C1_world, C2_world:
        camera centers in world coordinates.

    Rectified camera convention
    ---------------------------
    x-axis: points along the stereo baseline in world coordinates
    y-axis: points approximately along the old camera image-down direction
    z-axis: points forward, orthogonal to x and y

    R_rect_c2w:
        rectified camera-to-world rotation.

    R_rect_w2c:
        rectified world-to-camera rotation.
    """

    C1_world = C1_world.reshape(3)
    C2_world = C2_world.reshape(3)


    """Choosing new extrinsics"""
    # Rectified camera x-axis in world coordinates.
    # (baseline direction from left camera center to right camera center)
    x_axis_world = C2_world - C1_world
    x_axis_world /= np.linalg.norm(x_axis_world)

    # Original camera y-axis in world coordinates.
    y1_axis_world = R1_c2w[:, 1]
    y2_axis_world = R2_c2w[:, 1]
    y_old_world = 0.5 * (y1_axis_world + y2_axis_world)
    y_old_world /= np.linalg.norm(y_old_world)

    # Rectified camera y-axis in world coordinates.
    # It should stay close to the old image-down direction,
    # but it must be orthogonal to the new x-axis.
    y_axis_world = y_old_world - np.dot(y_old_world, x_axis_world) * x_axis_world
    y_axis_world /= np.linalg.norm(y_axis_world)

    # Rectified camera z-axis in world coordinates.
    z_axis_world = np.cross(x_axis_world, y_axis_world)
    z_axis_world /= np.linalg.norm(z_axis_world)

    # Rectified camera-to-world rotation.
    R_rect_c2w = np.column_stack([
        x_axis_world,
        y_axis_world,
        z_axis_world,
    ])

    # Rectified world-to-camera rotation.
    R_rect_w2c = R_rect_c2w.T


    """Choosing new intrinsics"""
    # This keeps approximately the same focal length and principal point.
    K_new = 0.5 * (K1 + K2)
    K_new[0, 1] = 0.0

    """
    Homographies (Old image pixels ==> rectified image pixels)
    ----------------------------------------------------------
    
    old pixel            ==> old camera ray           | ray_old_camera  = inv(K_old) @ pixel_old
    old camera ray       ==> world ray                | ray_world       = R_old_c2w  @ ray_old_camera
    world ray            ==> rectified camera ray     | ray_rect_camera = R_rect_w2c @ ray_world
    rectified camera ray ==> rectified pixel          | pixel_rect      = K_new      @ ray_rect_camera
    """

    H1 = K_new @ R_rect_w2c @ R1_c2w @ np.linalg.inv(K1)
    H2 = K_new @ R_rect_w2c @ R2_c2w @ np.linalg.inv(K2)


    return H1, H2



def compute_rectification(left_img, right_img, K_left, K_right, R_left, R_right, T_left, T_right):
    height, width = left_img.shape[:2]

    # Rectifying Homography which makes epipolar lines horizontal
    H_left, H_right = stereo_rectify_no_cv2(
        K_left, K_right,
        R_left, R_right,
        T_left, T_right,
    )

    # Shearing transformation for horizontal undistortion
    S_left = loop_zhang_shear(H_left, width, height)
    S_right = loop_zhang_shear(H_right, width, height)    

    # Combining all transformations
    H_left = S_left @ H_left
    H_right = S_right @ H_right

    left_rectified, right_rectified, H_left_shifted, H_right_shifted = (
        tight_warp(
            left_img, right_img,
            H_left, H_right,
            width, height,
            border_value=(1,1,1)
        )
    )
    return left_rectified, right_rectified, H_left_shifted, H_right_shifted

if __name__ == "__main__":
    left_img = plt.imread("blender/images/left.png")
    right_img = plt.imread("blender/images/right.png")

    height, width = left_img.shape[:2]

    K_left, R_left, T_left = get_calibration("blender/calibration/left_cal")
    K_right, R_right, T_right = get_calibration("blender/calibration/right_cal")

    left_rectified, right_rectified, H_left_shifted, H_right_shifted = compute_rectification(
        left_img,
        right_img,
        K_left,
        K_right,
        R_left,
        R_right,
        T_left,
        T_right,
    )

    cv2.imwrite("left_rectified.png", cv2.cvtColor(left_rectified * 255, cv2.COLOR_RGB2BGR))
    cv2.imwrite("right_rectified.png", cv2.cvtColor(right_rectified * 255, cv2.COLOR_RGB2BGR))
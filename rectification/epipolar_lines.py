import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils import get_calibration
from epipolar_geometry import compute_fundamental_matrix, rectification_homography


def transformed_corners(H, width, height):
    corners = np.array(
        [
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1],
        ],
        dtype=np.float32,
    ).reshape(-1, 1, 2)

    warped = cv2.perspectiveTransform(corners, H)
    return warped.reshape(-1, 2)


def stereo_tight_warp(
    left_img,
    right_img,
    H_left,
    H_right,
    width,
    height,
    border_value=(255, 255, 255),
):
    corners_left = transformed_corners(H_left, width, height)
    corners_right = transformed_corners(H_right, width, height)

    all_corners = np.vstack([corners_left, corners_right])

    min_corner = np.floor(all_corners.min(axis=0)).astype(int)
    max_corner = np.ceil(all_corners.max(axis=0)).astype(int)

    new_width = max_corner[0] - min_corner[0]
    new_height = max_corner[1] - min_corner[1]
    new_size = (new_width, new_height)

    shared_shift = np.array(
        [
            [1, 0, -min_corner[0]],
            [0, 1, -min_corner[1]],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    H_left_shifted = shared_shift @ H_left
    H_right_shifted = shared_shift @ H_right

    left_rectified = cv2.warpPerspective(
        left_img,
        H_left_shifted,
        new_size,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )

    right_rectified = cv2.warpPerspective(
        right_img,
        H_right_shifted,
        new_size,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )

    return left_rectified, right_rectified, H_left_shifted, H_right_shifted


def valid_x_range_from_mask(H, width, height, new_size):
    mask = np.ones((height, width), dtype=np.uint8) * 255

    warped_mask = cv2.warpPerspective(
        mask,
        H,
        new_size,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

    ys, xs = np.where(warped_mask > 0)

    return xs.min(), xs.max()


def midpoint_points(width, height):
    return [
        np.array([(width - 1) / 2, 0, 1.0]),
        np.array([width - 1, (height - 1) / 2, 1.0]),
        np.array([(width - 1) / 2, height - 1, 1.0]),
        np.array([0, (height - 1) / 2, 1.0]),
    ]


def affine_point(H, point):
    point_transformed = H @ point
    point_transformed /= point_transformed[-1]
    return point_transformed[:2]


def loop_zhang_shear(H, width, height):
    top, right, bottom, left = midpoint_points(width, height)

    top_t = affine_point(H, top)
    right_t = affine_point(H, right)
    bottom_t = affine_point(H, bottom)
    left_t = affine_point(H, left)

    x = right_t - left_t
    y = bottom_t - top_t

    x_u, x_v = x
    y_u, y_v = y

    w = width
    h = height

    denom = h * w * (x_u * y_v - x_v * y_u)

    if abs(denom) < 1e-12:
        return np.eye(3)

    s_a = (h * h * x_v * x_v + w * w * y_v * y_v) / denom
    s_b = -(h * h * x_u * x_v + w * w * y_u * y_v) / denom

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


left_img = plt.imread("blender/images/left.png")
right_img = plt.imread("blender/images/right.png")

height, width = left_img.shape[:2]

K_left, R_left, T_left = get_calibration("blender/calibration/left_cal")
K_right, R_right, T_right = get_calibration("blender/calibration/right_cal")

F = compute_fundamental_matrix(
    K1=K_left,
    K2=K_right,
    R1=R_left,
    R2=R_right,
    T1=T_left,
    T2=T_right,
)

R = R_right.T @ R_left
t = R_right.T @ (T_left - T_right)

R1, R2, P1, P2, _, _, _ = cv2.stereoRectify(
    cameraMatrix1=K_left,
    distCoeffs1=np.zeros(5),
    cameraMatrix2=K_right,
    distCoeffs2=np.zeros(5),
    imageSize=(width, height),
    R=R,
    T=t.reshape(3, 1),
)

# Rectifying Homography which makes epipolar lines horizontal
H_left = rectification_homography(K_left, R1, P1)
H_right = rectification_homography(K_right, R2, P2)

# Shearing transformation for horizontal undistortion
# S_left = loop_zhang_shear(H_left, width, height)
# S_right = loop_zhang_shear(H_right, width, height)    

# H_left = S_left @ H_left
# H_right = S_right @ H_right

left_rectified, right_rectified, H_left_shifted, H_right_shifted = stereo_tight_warp(
    left_img,
    right_img,
    H_left,
    H_right,
    width,
    height,
)

rect_h, rect_w = right_rectified.shape[:2]
new_size = (rect_w, rect_h)

left_x_min, left_x_max = valid_x_range_from_mask(
    H_left_shifted,
    width,
    height,
    new_size,
)

right_x_min, right_x_max = valid_x_range_from_mask(
    H_right_shifted,
    width,
    height,
    new_size,
)

left_vis = left_rectified[:, left_x_min:left_x_max + 1]
right_vis = right_rectified[:, right_x_min:right_x_max + 1]

gap = 0

if left_vis.ndim == 3:
    gap_img = np.ones((rect_h, gap, left_vis.shape[2]), dtype=left_vis.dtype)
else:
    gap_img = np.ones((rect_h, gap), dtype=left_vis.dtype)

if np.issubdtype(left_vis.dtype, np.floating):
    gap_img *= 1.0
else:
    gap_img *= 255

combined_rectified = np.concatenate([left_vis, gap_img, right_vis], axis=1)

top_gap = np.ones((height, gap, left_img.shape[2]), dtype=left_img.dtype)

if np.issubdtype(left_img.dtype, np.floating):
    top_gap *= 1.0
else:
    top_gap *= 255

top_combined = np.concatenate([left_img, top_gap, right_img], axis=1)

fig, axs = plt.subplots(2, 1, figsize=(14, 8))

axs[0].imshow(top_combined)
axs[0].set_title("Original left and right")

axs[1].imshow(combined_rectified)
axs[1].set_title("Rectified left and right, compact visualization")

for ax in axs:
    ax.axis("off")

plt.tight_layout()
plt.show()
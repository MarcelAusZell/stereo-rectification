import numpy as np
import matplotlib.pyplot as plt
from utils import get_calibration
from epipolar_geometry import compute_fundamental_matrix
from rectification import compute_rectification

def epipolar_line_endpoints(a, b, c, width, height):
    """
    Line equation in general case:
        a*x + b*y + c = 0
        b*y = -(a*x + c)
        y   = -(a*x + c) / b
    Choose two x-values on the image borders:
        x0 = 0
        x1 = width - 1
    Special case: b approx 0
        a*x + b*y + c = 0
        a*x + c = 0
        x = -c/a
    So x is constant which is a vertical line and vary y from top to bottom of the image
    """
    if abs(b) > 1e-12:
        x0 = 0
        y0 = -(a * x0 + c) / b

        x1 = width - 1
        y1 = -(a * x1 + c) / b

        return (x0, x1), (y0, y1)
    else:
        x = -c / a
        return (x, x), (0, height - 1)

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



num_points = 5
fig, axs = plt.subplots(1,2)
for ax in axs: ax.axis("off")
axs[0].imshow(left_img)
axs[1].imshow(right_img)
plt.sca(axs[0])
colors = ["red", "cyan", "lime", "orange", "hotpink"]
for i in range(num_points):
    point = fig.ginput(1)[0]
    u,v = point
    
    axs[0].scatter(x=u, y=v, c=colors[i], marker="+", s=60, lw=2)


    coordinate = np.array([u,v,1.0])
    a,b,c = F @ coordinate
    x_vals, y_vals = epipolar_line_endpoints(a, b, c, width, height)
    axs[1].plot(x_vals, y_vals, c=colors[i])

for i, ax in enumerate(axs):
    extent = ax.get_window_extent().transformed(
        fig.dpi_scale_trans.inverted()
    )

    fig.savefig(
        f"axis_{i}.png",
        bbox_inches=extent,
        dpi=400
    )
plt.show()

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
height_rect, width_left_rect = left_rectified.shape[:2]
_, width_right_rect = right_rectified.shape[:2]

num_points = 5
fig, axs = plt.subplots(1, 2)

for ax in axs:
    ax.axis("off")

axs[0].imshow(left_rectified)
axs[1].imshow(right_rectified)

plt.sca(axs[0])

colors = ["red", "cyan", "lime", "orange", "hotpink"]

for i in range(num_points):
    u_rect, v_rect = fig.ginput(1)[0]

    axs[0].scatter(
        u_rect, v_rect,
        c=colors[i],
        marker="+",
        s=60,
        lw=2,
    )

    axs[1].axhline(
        y=v_rect,
        c=colors[i],
        lw=2,
    )
for i, ax in enumerate(axs):
    extent = ax.get_window_extent().transformed(
        fig.dpi_scale_trans.inverted()
    )

    fig.savefig(
        f"axis_rec_{i}.png",
        bbox_inches=extent,
        dpi=400
    )
plt.show()
import bpy
import numpy as np

def export_camera(cam_name, filepath):
    cam = bpy.data.objects[cam_name]
    scene = bpy.context.scene

    w = scene.render.resolution_x
    h = scene.render.resolution_y

    cam_data = cam.data

    f_mm = cam_data.lens
    sensor_w = cam_data.sensor_width
    sensor_h = cam_data.sensor_height

    fx = f_mm / sensor_w * w
    fy = f_mm / sensor_h * h
    cx = w / 2
    cy = h / 2

    R_b2cv = np.array([
        [1, 0, 0],
        [0,-1, 0],
        [0, 0,-1],
    ])

    R_blender = np.array(cam.matrix_world.to_3x3())
    T = np.array(cam.matrix_world.to_translation())

    R = R_blender @ R_b2cv.T

    with open(filepath, "w") as f:
        f.write(f"u0 = {cx}\n")
        f.write(f"v0 = {cy}\n")
        f.write(f"au = {fx}\n")
        f.write(f"av = {fy}\n")
        f.write(str(R.tolist()).replace("[", "{").replace("]", "}") + "\n")
        f.write(str(T.tolist()).replace("[", "{").replace("]", "}") + "\n")


export_camera("left", "calibration/left_cal")
export_camera("right", "calibration/right_cal")
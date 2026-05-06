import re
import numpy as np


def get_calibration(file_path):
  """
  Looks at calibration file under file_path and returns intrinsics and extrinsics
  """
  file_str = ""

  with open(file=file_path, mode="r") as file: 
    file_str = file.read()

  u0 = re.search(r"u0 = \d+.\d+", file_str)
  v0 = re.search(r"v0 = \d+.\d+", file_str)
  au = re.search(r"au = \d+.\d+", file_str)
  av = re.search(r"av = \d+.\d+", file_str)
  rotation = re.search(r"\{\{.*?\}\}", file_str, re.DOTALL)
  translation = eval(file_str.strip().split("\n")[-1].replace("{", "[").replace("}", "]"))

  if u0:
    cx = float(u0.group()[5:])
  if v0:
    cy = float(v0.group()[5:])
  if au:
    fx = float(au.group()[5:])
  if av:
    fy = float(av.group()[5:])
  if rotation:
    rotation = eval(rotation.group().replace("{", "[").replace("}", "]"))

  K = np.array(
    [
      [fx,0,cx],
      [0,fy,cy],
      [0,0,1]
    ]
  )
  R = np.array(rotation)
  T = np.array(translation)
  return K,R,T


    
def draw_epipolar_line(ax, line, img_shape, x_offset=0, color="r"):
    h, w = img_shape[:2]
    a, b, c = line.astype(float)

    points = []

    if abs(b) > 1e-12:
        for x in [0, w - 1]:
            y = -(a * x + c) / b
            if 0 <= y < h:
                points.append((x, y))

    if abs(a) > 1e-12:
        for y in [0, h - 1]:
            x = -(b * y + c) / a
            if 0 <= x < w:
                points.append((x, y))

    if len(points) >= 2:
        p1, p2 = points[:2]
        ax.plot(
            [p1[0] + x_offset, p2[0] + x_offset],
            [p1[1], p2[1]],
            color=color
        )
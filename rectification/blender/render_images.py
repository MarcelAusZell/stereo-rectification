import bpy

scene = bpy.context.scene

cam_left = bpy.data.objects["left"]
cam_right = bpy.data.objects["right"]

for cam in [cam_left, cam_right]:
  scene.camera = cam
  scene.render.filepath = f"//images//{cam.name}.png"
  bpy.ops.render.render(write_still=True)
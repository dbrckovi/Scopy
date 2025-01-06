import time, libcamera
from picamera2 import Picamera2, Preview
import numpy as np
import scope_overlay
import fan_control

picam2 = None
streaming = False
full_res = None
view_rect = None
move_pixels = 15
zoom_factor_delta = 0.99
stream_aspect_ratio = 1

STREAM_WIDTH = 1920 
STREAM_HEIGHT = 1080

def start():
  global picam2
  global streaming
  global full_res
  global stream_aspect_ratio
  global STREAM_WIDTH  
  global STREAM_HEIGHT 

  OS_PANEL_HEIGHT = 36
  WINDOW_TITLE_HEIGHT = 28
  WINDOW_WIDTH = 1920
  WINDOW_HEIGHT = 1080 - OS_PANEL_HEIGHT
  STREAM_WIDTH = WINDOW_WIDTH
  STREAM_HEIGHT = WINDOW_HEIGHT - WINDOW_TITLE_HEIGHT
  stream_aspect_ratio = STREAM_WIDTH / STREAM_HEIGHT

  if not streaming:
    picam2 = Picamera2()
    #config = picam.create_preview_configuration(main={"size": (STREAM_WIDTH, STREAM_HEIGHT)})
    
    preview_config = picam2.create_preview_configuration(main={"size": (STREAM_WIDTH, STREAM_HEIGHT)})
    preview_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam2.configure(preview_config)
    picam2.start_preview(Preview.QTGL, x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    picam2.start()
    full_res = picam2.camera_properties['PixelArraySize']
    streaming = True
    print("Started streaming")
    print("  Camera:")
    print("    Full resolution: ", full_res)
    print("    Aspect ratio: ", full_res[0] / full_res[1])
    print("  Stream:")
    print("    Full resolution: ", (STREAM_WIDTH,STREAM_HEIGHT))
    print("    Aspect ratio: ", stream_aspect_ratio)

    set_minimal_zoom_center()
    refresh_overlay()

def stop():
  global picam2
  global streaming

  if streaming:
    picam2.stop()
    picam2.close()
    streaming = False
    print("Stopped streaming")

def set_normal_zoom_center():       # zooms in to center, so that one pixel from camera equals one pixel on screen
  view_size = (STREAM_WIDTH, STREAM_HEIGHT)
  center = (int(full_res[0] / 2), int(full_res[1] / 2))
  set_view_center(view_size, center)

def set_minimal_zoom_center():
  x = full_res[0]
  y = int(x / stream_aspect_ratio)
  center = (int(full_res[0] / 2), int(full_res[1] / 2))
  set_view_center((x,y), center)

# Attempts to move current view rectangle so that it's centered around given camera coordinate
# If view is larger than screen size, resets the view to normal zoom center
def set_view_center(view_size, center):    
  view_width = view_size[0]
  view_height = view_size[1]
  if view_width > full_res[0] or view_height > full_res[1]:
    return

    #set_normal_zoom_center()
  else:
    x = center[0] - int(view_width / 2)
    y = center[1] - int(view_height / 2)

    if x < 0: x = 0
    if x + view_width > full_res[0]: x = full_res[0] - view_width
    if y < 0: y = 0
    if y + view_height > full_res[1]: y = full_res[1] - view_height

    set_view_region((x,y,view_width,view_height))
  
def set_view_region(new_rect):    # (left, top, width, height)
  global view_rect
  view_rect = new_rect
  picam2.set_controls({"ScalerCrop": view_rect})
  refresh_overlay()

def move_up():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]

  top = top - move_pixels
  if top < 0:
    top = 0

  set_view_region((left, top, width, height))

def move_down():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]

  top = top + move_pixels
  if top + height > full_res[1]:
    top = full_res[1] - height

  set_view_region((left, top, width, height))

def move_left():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]

  left = left - move_pixels
  if left < 0:
    left = 0

  set_view_region((left, top, width, height))

def move_right():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]

  left = left + move_pixels
  if left + width > full_res[0]:
    left = full_res[0] - width

  set_view_region((left, top, width, height))

def zoom_in():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]
  centerX = left + int(width / 2)
  centerY = top + int(height / 2)

  width = int(width * zoom_factor_delta)
  height = int(height * zoom_factor_delta)

  zoom = STREAM_WIDTH / width
  if (zoom <= 4):
    set_view_center((width,height),(centerX,centerY))

def zoom_out():
  left = view_rect[0]
  top = view_rect[1]
  width = view_rect[2] 
  height = view_rect[3]

  centerX = left + int(width / 2)
  centerY = top + int(height / 2)
  width = int(width / zoom_factor_delta)
  height = int(height / zoom_factor_delta)

  set_view_center((width,height),(centerX,centerY))

def refresh_overlay():
  if streaming:
    try:
      topLine = "ScoPy    [HOLD OFF] - shutdown     [Double +] - normal zoom     [Double -] - full view"

      z = "Z: {:.2f}".format(STREAM_WIDTH / view_rect[2])
      x = ",   X: " + str(view_rect[0])
      y = ",   Y: " + str(view_rect[1])
      w = ",   W: " + str(view_rect[2])
      h = ",   H: " + str(view_rect[3])
      t = ",   T: {:.2f} C".format(fan_control.getTemperature())
      fan = "" 
      if fan_control.isFanOn(): fan = "    FAN ON"

      bottomLine = z + x + y + w + h + t + fan

      overlay = scope_overlay.render_overlay(topLine, bottomLine)
      picam2.set_overlay(overlay)
    except TypeError:  
      print("Error while rendering overlay")

import time
import camera
import in_out
import fan_control

should_exit = False
off_button_press_time = None
last_plus_release = None
last_minus_release = None
DOUBLE_CLICK_TRESHOLD = 500

def button_pressed(button):
  global off_button_press_time
  
  if button == in_out.BTN_ONOFF:
    off_button_press_time = time.time()

  if button == in_out.BTN_DOWN:
    camera.move_down()

  if button == in_out.BTN_UP:
    camera.move_up()

  if button == in_out.BTN_LEFT:
    camera.move_left()

  if button == in_out.BTN_RIGHT:
    camera.move_right()

  if button == in_out.BTN_PLUS:
    camera.zoom_in()

  if button == in_out.BTN_MINUS:
    camera.zoom_out()        

def button_released(button):
  global last_plus_release
  global last_minus_release

  if button == in_out.BTN_ONOFF:
    if not camera.streaming:
      #start stream
      camera.start()
      in_out.setOutput(in_out.LED_STREAMING, True)  
    else:
      #stop stream
      if not should_exit: #if you hold BTN_ONOFF for exactly 2 seconds, and then release, camera.stop() might throw exception without this check
        camera.stop()
        in_out.setOutput(in_out.LED_STREAMING, False)  

  if button == in_out.BTN_PLUS:
    if not last_plus_release:
      last_plus_release = time.time()
    else: 
      elapsed_time = (time.time() - last_plus_release) * 1000
      if (elapsed_time < DOUBLE_CLICK_TRESHOLD):
        camera.set_normal_zoom_center()
      else:
        last_plus_release = time.time()  

  if button == in_out.BTN_MINUS:
    if not last_minus_release:
      last_minus_release = time.time()
    else: 
      elapsed_time = (time.time() - last_minus_release) * 1000
      if (elapsed_time < DOUBLE_CLICK_TRESHOLD):
        camera.set_minimal_zoom_center()
      else:
        last_minus_release = time.time()  

def button_repeat(button):
  global should_exit
  global off_button_press_time

  if button == in_out.BTN_ONOFF:
    elapsed_time = (time.time() - off_button_press_time) * 1000
    if (elapsed_time > 2000):
      should_exit = True

  if button == in_out.BTN_DOWN:
    camera.move_down()

  if button == in_out.BTN_UP:
    camera.move_up()

  if button == in_out.BTN_LEFT:
    camera.move_left()

  if button == in_out.BTN_RIGHT:
    camera.move_right()

  if button == in_out.BTN_PLUS:
    camera.zoom_in()

  if button == in_out.BTN_MINUS:
    camera.zoom_out()      

#MAIN
print("Scope started")
last_temperature_refresh = time.time()
in_out.setOnButtonPressed(button_pressed)
in_out.setOnButtonReleased(button_released)
in_out.setOnButtonRepeat(button_repeat)
in_out.initialize()
in_out.setOutput(in_out.LED_ON, True)

while should_exit == False:
  fan_control.checkTemperature()

  temperature_refresh_elapsed = (time.time() - last_temperature_refresh) * 1000
  if (temperature_refresh_elapsed > 3000):
    camera.refresh_overlay()
    last_temperature_refresh = time.time()

  time.sleep(0.01)

camera.stop()
fan_control.cleanup()
in_out.cleanup()

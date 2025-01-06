import time
import RPi.GPIO as GPIO
import threading

"""
Raspberry Pi 4 pinout:
           3V3  (1) (2)  5V    
         GPIO2  (3) (4)  5V    
 [SDA]   GPIO3  (5) (6)  GND   
         GPIO4  (7) (8)  GPIO14   [TXD]
           GND  (9) (10) GPIO15   [RXD]
 [PoE]  GPIO17 (11) (12) GPIO18
 [EPR]  GPIO27 (13) (14) GND      GND for buttons
        GPIO22 (15) (16) GPIO23   {BTN_MINUS}   //Zoom out
           3V3 (17) (18) GPIO24   {BTN_PLUS}    //Zoom in
        GPIO10 (19) (20) GND   
         GPIO9 (21) (22) GPIO25   {BTN_DOWN}
        GPIO11 (23) (24) GPIO8    {BTN_UP} 
           GND (25) (26) GPIO7    {BTN_RIGHT} 
         GPIO0 (27) (28) GPIO1    {BTN_ON} 
 [SCL]   GPIO5 (29) (30) GND       
         GPIO6 (31) (32) GPIO12   {BTN_LEFT} 
        GPIO13 (33) (34) GND      GND for fan and leds 
        GPIO19 (35) (36) GPIO16   {LED_FAN}
        GPIO26 (37) (38) GPIO20   {LED_STREAMING}
           GND (39) (40) GPIO21   {LED_ON}
"""

LED_ON = 21
LED_STREAMING = 20
FAN_ON = 16
BTN_ONOFF = 1
BTN_UP = 8
BTN_DOWN = 25
BTN_LEFT = 12
BTN_RIGHT = 7
BTN_PLUS = 24
BTN_MINUS = 25

PRESSED_REPEAT_TIME = 30

on_button_pressed = None
on_button_released = None
on_button_repeat = None

shouldRun = False
button_thread = None

def initialize():
  global button_thread
  global shouldRun
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(LED_ON, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(LED_STREAMING, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(FAN_ON, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(BTN_ONOFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_PLUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTN_MINUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  button_thread = threading.Thread(target=button_loop)
  button_thread.daemon = True
  shouldRun = True
  button_thread.start()

def setOutput(pin, state):
  GPIO.output(pin, state)

def cleanup():
  global shouldRun
  shouldRun = False
  button_thread.join()
  GPIO.cleanup()

def setOnButtonPressed(callback):
  global on_button_pressed
  on_button_pressed = callback

def setOnButtonReleased(callback):
  global on_button_released
  on_button_released = callback

def setOnButtonRepeat(callback):
  global on_button_repeat
  on_button_repeat = callback

def button_loop():
  global shouldRun
  button_times = {}
  
  while shouldRun:
    for button in [BTN_ONOFF, BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT, BTN_PLUS, BTN_MINUS]:
      new_state = not GPIO.input(button)
      old_state = button in button_times

      if new_state != old_state:
        if new_state:
          button_times[button] = time.time()
          if on_button_pressed:
            on_button_pressed(button)   # pressed
          
        else:
          del button_times[button]
          if on_button_released:
            on_button_released(button)  # released
          
      elif new_state:
        elapsed_time = (time.time() - button_times[button]) * 1000
        if elapsed_time > PRESSED_REPEAT_TIME:
          button_times[button] = time.time()
          if on_button_repeat:
            on_button_repeat(button)    # repeat
           
    time.sleep(0.01) 

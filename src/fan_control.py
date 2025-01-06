import in_out
import time
import camera

last_on_time = None
HIGH_TEMPERATURE = 50
LOW_TEMPERATURE = 48
MIN_FAN_ON_TIME = 10

def isFanOn():
  if not last_on_time: return False
  else: return True 

def getTemperature():
  with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
    temp = int(file.read().strip())  
    temp_celsius = temp / 1000.0
    return temp_celsius

def checkTemperature():
  global last_on_time

  temp_celsius = getTemperature()

  if temp_celsius > HIGH_TEMPERATURE:
    if  last_on_time is None:
      in_out.setOutput(in_out.FAN_ON, True)
      last_on_time = time.time()
      print(temp_celsius)
      print("Turned on fan")
      camera.refresh_overlay()

  if temp_celsius < LOW_TEMPERATURE:
    if last_on_time is not None and (time.time() - last_on_time >= MIN_FAN_ON_TIME):
      in_out.setOutput(in_out.FAN_ON, False)
      last_on_time = None
      print(temp_celsius)
      print("Turned Off fan")  
      camera.refresh_overlay()

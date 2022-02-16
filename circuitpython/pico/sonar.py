# RVR drive sonar distance code 20 seconds with led output for raspberry pico

import board
import time
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP10, echo_pin=board.GP11)

sensor_distance = sonar.distance
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

while(elapsed_time < 20.0):
    elapsed_time = time.monotonic() - start_time
    try:
        sensor_distance = sonar.distance
        print(sensor_distance)
        led.value = True
        time.sleep(0.02)
        led.value = False
        time.sleep(sensor_distance / 200)

    except RuntimeError:
        print("Retrying!")
        pass
    time.sleep(0.2)

# RVR servo example for raspberry pico

import time
import board
import pwmio
import digitalio
from adafruit_motor import servo

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.GP28, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

while True:
    led.value = True
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.05)
    led.value = False
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.05)
        

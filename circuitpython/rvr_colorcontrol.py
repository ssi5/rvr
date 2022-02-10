# blink three times at startup on blackpill

import time
import board
import digitalio

def blink(blinks):
    led = digitalio.DigitalInOut(board.C13)
    led.direction = digitalio.Direction.OUTPUT
    for x in range(blinks):
        led.value = False
        time.sleep(0.2)
        led.value = True
        time.sleep(0.2)

blink(2)

import microcontroller

print("This is a Blackpill, running at {:.1f} MHz".format(float(microcontroller.cpu.frequency)/1000000))
print("The CPU has a temperature of {:.1f} °C.".format(microcontroller.cpu.temperature))

import sphero_rvr

print("I imported the sphero_rvr")

rvr = sphero_rvr.RVRDrive()
import gc
print(gc.mem_free())

while True:
    for x in range(255):
        rvr.set_all_leds(x,255-x,255-x)
    for x in range(255):
        rvr.set_all_leds(255-x,x,255-x)
    for x in range(255):
        rvr.set_all_leds(255-x,255-x,x)
    for x in range(255,0,-1):
        rvr.set_all_leds(x,x,x)
    

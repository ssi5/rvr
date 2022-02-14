# rvr

Control the Sphero RVR over the serial port, using Circuitpython. Since it is similar to Micropython, we can use parts of code for the micro:bit

## sphero.py for micro:bit

This is the raw file with 4 kByte and several functions we like to use. Uploaded as `sphero.py` from October 9, 2019 ([link to Github](https://github.com/sphero-inc/sphero-sdk-microbit-python/blob/master/sphero.py)):

``` py
from microbit import uart

class LEDs:
    RIGHT_HEADLIGHT    = [0x00, 0x00, 0x00, 0x07]  # 00000000 00000000 00000000 00000111
    LEFT_HEADLIGHT     = [0x00, 0x00, 0x00, 0x38]  # 00000000 00000000 00000000 00111000
    LEFT_STATUS        = [0x00, 0x00, 0x01, 0xC0]  # 00000000 00000000 00000001 11000000
    RIGHT_STATUS       = [0x00, 0x00, 0x0E, 0x00]  # 00000000 00000000 00001110 00000000
    BATTERY_DOOR_FRONT = [0x00, 0x03, 0x80, 0x00]  # 00000000 00000000 01110000 00000000
    BATTERY_DOOR_REAR  = [0x00, 0x00, 0x70, 0x00]  # 00000000 00000011 10000000 00000000
    POWER_BUTTON_FRONT = [0x00, 0x1C, 0x00, 0x00]  # 00000000 00011100 00000000 00000000
    POWER_BUTTON_REAR  = [0x00, 0xE0, 0x00, 0x00]  # 00000000 11100000 00000000 00000000
    LEFT_BRAKELIGHT    = [0x07, 0x00, 0x00, 0x00]  # 00000111 00000000 00000000 00000000
    RIGHT_BRAKELIGHT   = [0x38, 0x00, 0x00, 0x00]  # 00111000 00000000 00000000 00000000

class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2

class RVRDrive:
    @staticmethod
    def drive(speed, heading):
        flags = 0x00
        if speed < 0:
            speed *= -1
            heading += 180
            heading %= 360
            flags = 0x01
        drive_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x07, 0x00,
            speed, heading >> 8, heading & 0xFF, flags
        ]
        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(drive_data))
        return

    @staticmethod
    def stop(heading):
        RVRDrive.drive(0, heading)
        return

    @staticmethod
    def set_raw_motors(left_mode, left_speed, right_mode, right_speed):
        if left_mode < 0 or left_mode > 2:
            left_mode = 0
        if right_mode < 0 or right_mode > 2:
            right_mode = 0
        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x01, 0x00,
            left_mode, left_speed, right_mode, right_speed
        ]
        raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(raw_motor_data))
        return

    @staticmethod
    def reset_yaw():
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]
        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(drive_data))
        return

class RVRLed:
    @staticmethod
    def set_all_leds(red, green, blue):
        led_data = [
            0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00,
            0x3F, 0xFF, 0xFF, 0xFF
        ]
        
        for _ in range (10):
            led_data.extend([red, green, blue])
        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(led_data))
        return

    @staticmethod
    def set_rgb_led_by_index(index, red, green, blue):
        led_data = [0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00]
        led_data.extend(index)
        led_data.extend([red, green, blue])
        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(led_data))
        return

class RVRPower:
    @staticmethod
    def wake():
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x0D, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(power_data))
        return
        
    @staticmethod
    def sleep():
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x01, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        uart.write(bytearray(power_data))
        return
```

- RVRDrive with
  - drive(*speed, heading*)
  - stop(*heading*)
  - set_raw_motors(*left_mode, left_speed, right_mode_ right_speed*)
  - `reset_yaw()`
- RVRLed for the 10 LEDs with `.set_all_leds` and `.set_rgb_led_by_index`
- RVRPower with `.sleep()` and `.wake()`


## Documentation of protocol and code

The packages are well documented by [@emwdx](https://github.com/emwdx) in his code for `drive_to_position`:

``` py
# Set up the serial port on the board
uart = busio.UART(board.TX, board.RX, baudrate=115200)

# This function takes in an angle, a pair of x and y coordinates, and a speed target to use for the RVR.
def drive_to_position_si(yaw_angle, x, y, speed):

  # This sets up the list of bytes needed for this command to be sent to the RVR through the serial port.
    SOP = 0x8d             # Always the start byte for a command to the RVR
    FLAGS = 0x06           # This tells the RVR to ignore the target and source ID, 
	                       # and that this command expects a response only if there are errors.
    TARGET_ID = 0x0e 
    SOURCE_ID = 0x0b
    DEVICE_ID = 0x16       # The drive system ID is 0x16
    COMMAND_ID = 0x38      # The drive_to_position_si command has ID of 38
    SEQ = 0x01             # The sequence value is arbitrarily 1. We aren't using the sequence capability here.
    EOP = 0xD8             # The final byte in the command is 0xD8

  # The command expects four float values for yaw angle, x coordinate, y coordinate, and speed. 
  # This lets you use decimal values.
  # The lines below convert the float values to a set of four bytes representing each value.
    yaw_angle = bytearray(struct.pack('>f', yaw_angle))
    x = bytearray(struct.pack('>f', x))
    y = bytearray(struct.pack('>f', y))
    speed = bytearray(struct.pack('>f', speed))
	
  # The command has a flags byte that lets you set different attributes for how the robot moves 
  # between the positions. Check out page 12 of the SpheroRVRControlSystem manual for the details.
    flags = bytearray(struct.pack('B', 0))

  # Now we build the command packet byte by byte. First the first five bytes:
    output_packet = [SOP, FLAGS, DEVICE_ID, COMMAND_ID, SEQ]

  # Now the bytes for the flags
    output_packet.extend(yaw_angle)
    output_packet.extend(x)
    output_packet.extend(y)
    output_packet.extend(speed)
    output_packet.extend(flags)
  # And the checksum byte which does some math with the sum of the previous 
  # bytes in the command, and finally the end of packet byte.
    output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,EOP])

  # Now that the command is complete, return the command as an array of bytes.
    return bytearray(output_packet)

# END OF DRIVE_TO_POSITION_SI
```

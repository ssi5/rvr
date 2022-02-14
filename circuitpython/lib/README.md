# rvr
Control the Sphero RVR over the serial port, using Circuitpython

## Documentation of protocol and code

The packages are well documented by [@emwdx](https://github.com/emwdx) in his code:

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
    output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]

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

Further documentation in [this presentation](https://drive.google.com/file/d/1oYMbidrGnvpz_ruhsh2HalU-BsVFMmpa/view?usp=sharing).

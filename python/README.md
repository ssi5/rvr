# Controlling the Sphero RVR using Python

The rvr can be controlled via the serial port. The command structure is rather sophisticated and the number of commands, methods and functions quite long. The possible options are not that extensive, but it seems the SDK was intended to be more complex than needed and is lacking a lot of functionality. Three microcontrollers can be used: __micro:bit__ with *MicroPython* (no library exist), Arduino in *C* (unnecessarily complicated for a few basic functions) and __Raspberry Pi__ with *Python* ().

It seems it was a little ambitious, but now many parts are deprecated and inactive: [https://github.com/sphero-inc](https://github.com/sphero-inc)

## micro:bit

This SDK seems to be non existent. Documentation at [https://sdk.sphero.com/docs/getting_started/microbit/microbit_setup](https://sdk.sphero.com/docs/getting_started/microbit/microbit_setup) contains no link to the actual library you could import or a single example line.

But then I found the github repository: [https://github.com/sphero-inc/sphero-sdk-microbit-python](https://github.com/sphero-inc/sphero-sdk-microbit-python)

This is perfect for our Circuitpython project!! The micro:bit is even more limited in RAM than our M0 Metro express, let's copy the short function files:

- RVRDrive with
  - drive(*speed, heading*)
  - stop(*heading*)
  - set_raw_motors(*left_mode, left_speed, right_mode_ right_speed*)
  - reset_yaw()
- RVRLed for the 10 LEDs with .set_all_leds and .set_rgb_led_by_index
- RVRPower with .sleep() and .wake()

All these funtions are defined in this little short file `sphero.py` from October 9, 2019 ([link to Github](https://github.com/sphero-inc/sphero-sdk-microbit-python/blob/master/sphero.py)):

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

## Raspberry Pi python library

You can get the `asyncio` version (33 files, 136 kByte) and the `observer` version (20 files, 112 kByte). The difference? And what about the `common` folder (48 fiels, 208 kByte)?


## Arduino library 

This library simply does not exist. Some information is written at [https://sdk.sphero.com/docs/getting_started/arduino/arduino_setup](https://sdk.sphero.com/docs/getting_started/arduino/arduino_setup) but the link to `SDK commands` or `Arduino SDK` are all the same: It lins to [https://sdk.sphero.com/how_to/arduino_how_to](https://sdk.sphero.com/how_to/arduino_how_to) with the Firebase answer __Page Not Found__. The correct link though is [https://sdk.sphero.com/docs/how_to/arduino/arduino_how_to](https://sdk.sphero.com/docs/how_to/arduino/arduino_how_to). The first steps are always:

``` c
#include <SpheroRVR.h>

void setup() {
  rvr.configUARD(&Serial);
}
```

### Driving
#### Driving with Raw Motors - 2 functions

- rvr.resetYaw();
- rvr.rawMotors(RawMotorModes::forward, 64, RawMotorModes::forward, 64);
- rvr.rawMotors(RawMotorModes::reverse, 32, RawMotorModes::reverse, 32);
- rvr.rawMotors(RawMotorModes::off, 0, RawMotorModes::off, 0);

The order is left motor, speed, right motor, speed.

#### Driving with Heading

``` c
// drive forward with speed 64
rvr.driveWithHeading(64, 0, static_cast<uint8_t>(DriveFlags.none));

// drive backward with speed 32
rvr.driveWithHeading(32, 0, static_cast<uint8_t>(DriveFlags.driveReverse));

// drive to the right with speed 64
rvr.driveWithHeading(64, 90, static_cast<uint8_t>(DriveFlags.none));
```

#### Drive with Helper

You need one extra line in the setup to get DriveControl

``` c
#include <SpheroRVR.h>

static DriveControl driveControl;

void setup() {
    rvr.configUART(&Serial);
    driveControl = rvr.getDriveControl();
}

void loop() {
    // reset the heading to zero
    driveControl.setHeading(0);
    
    // drive forward with speed 64
    driveControl.rollStart(0, 64);
    
    // drive to the right with speed 64
    driveControl.rollStart(90, 64);
    
    // stop driving
    driveControl.rollStop(270);
}
```
#### Drive with Raw Motors with Helper

``` c
// drive forward with speed 64 on both motors
driveControl.setRawMotors(rawMotorModes::forward, 64, rawMotorModes::forward, 64);
    
// drive backward with speed 64 on the left motor and forward with speed 64 on the right motor
driveControl.setRawMotors(rawMotorModes::reverse, 64, rawMotorModes::forward, 64);
    
// turn both motors off
driveControl.setRawMotors(rawMotorModes::off, 0, rawMotorModes::off, 0);
```

### LEDs

This is unnecessarily complicated. But here we go:

``` c
#include <SpheroRVR.h>
static LedControl ledControl;
void setup() {
    rvr.configUART(&Serial);
    ledControl = rvr.getLedControl();
}

void loop() {
    // set up the array of led indexes for both headlights
    uint8_t ledIndexes[] = {static_cast<uint8_t>(LEDs::rightHeadlightRed),
                            static_cast<uint8_t>(LEDs::rightHeadlightGreen),
                            static_cast<uint8_t>(LEDs::rightHeadlightBlue),
                            static_cast<uint8_t>(LEDs::leftHeadlightRed),
                            static_cast<uint8_t>(LEDs::leftHeadlightGreen),
                            static_cast<uint8_t>(LEDs::leftHeadlightBlue)};
    // set headlights to red and wait 1 second
    uint8_t redBrightnessValues[] = {0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00};
    ledControl.setLeds(ledIndexes, redBrightnessValues, sizeof(ledIndexes) / sizeof(ledIndexes[0]));
}
```
There is more, but really ... it's just LEDs!

### Power

You just want the battery voltage? It's as easy as these lines:

``` c
#include <SpheroRVR.h>
static void getBatteryVoltageStateCallback(GetBatteryVoltageStateReturn_t *batteryVoltageStateReturn);
void setup() {
    rvr.configUART(&Serial);                                  // set up communication with the RVR
    delay(2000);                                                  // give RVR time to wake up
    rvr.getBatteryVoltageState(getBatteryVoltageStateCallback);   // get the battery voltage state
}

void loop() {                       // must include this line if expecting a response from the RVR
    rvr.poll();
}

static void getBatteryVoltageStateCallback(GetBatteryVoltageStateReturn_t *batteryVoltageStateReturn)
{
    // put your code here to run when you get the battery voltage state
}
```

### System

This must be a __joke__. Just to get a string like `v1.3.17` for the version number you have a ridiculous number of lines, and it only tells you if it is larger than one with blinking LEDs:

``` c
#include <SpheroRVR.h>

static void getMainApplicationVersionCallback(GetMainApplicationVersionReturn_t *getMainApplicationVersionReturn);

void setup() {
    // set up communication with the RVR
    rvr.configUART(&Serial);
    
    // give RVR time to wake up
    delay(2000);
    
    // get the main application version for the Nordic processor
    rvr.getMainApplicationVersion(static_cast<uint8_t>(Processors::nordic), getMainApplicationVersionCallback);
}

void loop() {
    // must include this line if expecting a response from the RVR
    rvr.poll();
}

static void getMainApplicationVersionCallback(GetMainApplicationVersionReturn_t *getMainApplicationVersionReturn)
{
    // setting up the led group for both headlights
    uint32_t ledGroup = 0;
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::rightHeadlightRed));
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::rightHeadlightGreen));
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::rightHeadlightBlue));
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::leftHeadlightRed));
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::leftHeadlightGreen));
    ledGroup |= (1 << static_cast<uint8_t>(LEDs::leftHeadlightBlue));
    
    if (getMainApplicationVersionReturn->minor >= 1)
    {
        // set headlights to yellow if the y value in version x.y.z is 1 or greater
        uint8_t rgbArray[] = {0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00};
        rvr.setAllLeds(ledGroup, rgbArray, sizeof(rgbArray) / sizeof(rgbArray[0]));
    }
    else
    {
        // set headlights to pink if the y value in version x.y.z is less than 1
        uint8_t rgbArray[] = {0xFF, 0x00, 0xFF, 0xFF, 0x00, 0xFF};
        rvr.setAllLeds(ledGroup, rgbArray, sizeof(rgbArray) / sizeof(rgbArray[0]));
    }
}
```

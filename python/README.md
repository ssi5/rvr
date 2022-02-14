# Controlling the Sphero RVR using Python

The rvr can be controlled via the serial port. The command structure is rather sophisticated and the number of commands, methods and functions quite long. The documentation itself could be better. Here are the options:

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

# Pin connection definition Microcontroller - RVR

We use the following standard pins to communicate with the Sphero RVR:

|                    | blackpill | rp2040 | lilygo ESP32-S2 | Metro M4 express |
|--------------------|:---------:|:------:|:---------------:|:----------------:|
| UART TX            |     A2    |   GP4  |       IO1       |        D1        |
| UART RX            |     A3    |   GP5  |       IO2       |        D0        |
| Ultrasonic trigger |     B1    |  GP10  |       IO5       |        D11       |
| Ultrasonic echo    |     B0    |  GP11  |       IO4       |        D10       |

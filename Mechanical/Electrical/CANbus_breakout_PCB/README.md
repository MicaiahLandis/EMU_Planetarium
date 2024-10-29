# EMU Planetarium CANbus Breakout PCB

## Overview

This PCB is designed to connect to an Adafruit CANbus RP2040 and break out the GPIO pins to multiple JST connectors. It includes connectors for:
- **Two stepper controllers**
- **Two breakbeams**

The board provides input and passthrough plugs for CANbus H and L, as well as a 24V power supply connection. Remaining GPIO pins from the RP2040 are routed to extra mounting holes as spares. Additionally, there are two spare two-pin 5V and GND JST connectors.

## Pinout

- **J1** Six pin JST Plug for Stepper 1
- **J2** Six pin JST Plug for Stepper 2
- **J3** Three pin CAN + GND connector for feather
- **J4** CANbus JST connetor
- **J5** 5V Power JST connector
- **J6** 24V XT30 connector
- **J7** CANbus JST connetor
- **J8** 24V XT30 connector
- **J9** Spares D4 and D5
- **J10** Spares A0-A5
- **J11** 5V power for breakbeam 1 bulb JST connector
- **J12** 5V power for breakbeam 2 bulb JST connector
- **J13** Breakbeam reciever 1 three pin JST connector
- **J14** Breakbeam reciever 2 three pin JST connector
- **J15** Spares RX and TX
- **J16** Spares MOSI and MISO
- **J17** 5V Power JST connector
- **J18** 5V Power JST connector

- **Feather_RP1** Adafruit RP2040 Feather w/CAN (MCP25625)

## Images

## Schematic
![Schematic](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/CANbus_breakout_PCB/schematic.png)

## PCB
![PCB](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/CANbus_breakout_PCB/PCBeditor_image.png)
- KiCAD PCB editor image showing traces and footprints

## Renders
![PCB](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/CANbus_breakout_PCB/CANbus_breakout_front.png)
![PCB](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/CANbus_breakout_PCB/CANbus_breakout_back.png)
![PCB](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/CANbus_breakout_PCB/CANbus_breakout_wconnectors.png)



---

Created by [Micaiah Landis](http://micaiahlandis.com)

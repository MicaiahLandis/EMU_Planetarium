# EMU Planetarium Renovation 2024-2025
## Electrical System Overview

---

### Team
- [Micaiah Landis](http://micaiahlandis.com)
- Adam Stoltzfus

---

## Project Goals

- **Main Control**: Centralized control managed by a Raspberry Pi 4.
- **Communication**: CANbus communications enabled by Adafruit RP2040 Feather with CAN support.
- **Power Distribution**:
  - 5V and 24V supplies for stepper motors.
  - Additional voltage supplies to power various bulbs and components as required.
- **Reuse of Existing Components**:
  - Existing slip rings repurposed for CANbus communication and power transmission.
- **Relay and Module Placement**:
  - Relays for bulb control located with the Raspberry Pi at the base.
  - RP2040 Feathers strategically positioned on axes for convenience and accessibility.

---

## Images

### Image 1: [Slip rings and wiring at axis 1]
![Image 1](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/Sliprings_electrical.jpg)

### Image 2: [80 sliprings through axis 3 (Base)]
![Image 2](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/sliprings1.jpg)

---

## Entire Wiring pinout
- **Overview**: There are 80 wires connected to a bus bar at the base of the planetarium that connect to varius different motors, lights and controllers.
- This diagram defines each of them including their original use and their updated use.
- **Note**: While taking advantage of pins labeled "spare" I discoverd that several wires (25-30) were connected to another group of spares (42-47)
- I was not however able to figure out where or why they were connected so I used them as they are.

- ### Image 2: [Schematic_v1.03]
![Image 3](https://github.com/MicaiahLandis/EMU_Planetarium/blob/main/Mechanical/Electrical/schematic_v1.03.jpg)

---

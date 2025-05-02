# Adafruit Feather Code
For use on [Adafruit RP2040 CAN Bus Feather with MCP2515 CAN Controller](https://www.adafruit.com/product/5724)

To set up a new Feather board:
1. Download [CircuitPython](https://circuitpython.org/board/adafruit_feather_rp2040_can/).
2. Hold down the BOOT button, plug the board in (or start with it plugged in and instead press and release the RESET button), and continue to hold the BOOT button until a drive shows up.
3. Drag the CircuitPython .UF2 file to the drive.
4. CIRCUITPY/lib needs to contain the following modules (Download [this project bundle](https://learn.adafruit.com/adafruit-picowbell-can-bus-for-pico/circuitpython) and copy the lib contents over):
	5. adafruit_bus_device/
	6. adafruit_mcp2515/
7. Put the appropriate board's code in the code.py file, which runs by default.

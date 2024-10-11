# circuit python code for feather rp2040 CAN

import board
import busio
import digitalio
import adafruit_mcp2515
import time

# Set up SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CAN_CS)  # Chip select pin (update if needed)
#interrupt_pin = digitalio.DigitalInOut(board.)  # Interrupt pin (update if needed)

# Create the MCP2515 CAN bus object
can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)

# Set the CAN bus speed (e.g., 500 kbps)


print("Listening for CAN messages...")

# Main loop
while True:
    message = can.read_message()  # Attempt to read a message
    if message is not None:  # Check if a message was received
        print("Received CAN message:")
        print("ID:", hex(message.id))
        print("Data:", [hex(byte) for byte in message.data])
        break
    else:
        print("No message available.")
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage

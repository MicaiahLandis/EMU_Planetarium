import board
import busio
import digitalio
import pwmio
import adafruit_mcp2515
import time

# Set up SPI and Chip Select (CS) pin
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CAN_CS)  # Update with correct CS pin

# Initialize MCP2515 with 100 kbps speed
can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT  # Configure as output

# Main loop
while True:
    message = can.read_message()  # Read incoming CAN message
    if message is not None:  # If a message is received
        if message.id == 0x124:
            print(f"Received message: ID={hex(message.id)}, Data={message.data[0]}")
            while True:
                led.value = True
                time.sleep(0.5)
                led.value = False
                time.sleep(0.5)

# Write your code here :-)

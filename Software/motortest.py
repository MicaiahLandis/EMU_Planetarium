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

pin = digitalio.DigitalInOut(board.D10)
dirpin = digitalio.DigitalInOut(board.D11)
pin.direction = digitalio.Direction.OUTPUT  # Configure as output
dirpin.direction = digitalio.Direction.OUTPUT  # Configure as output

# Main loop
while True:
    message = can.read_message()  # Read incoming CAN message
    if message is not None:  # If a message is received
        print(f"Received message: ID={hex(message.id)}, Data={message.data[0]}")

        # Move motor at speeds based on incoming data value
        if message.data[0] == 1:
            sleep = 0.1
            limit = 10
            direction = True
        elif message.data[0] == 2:
            sleep = 0.01
            limit = 100
            direction = True
        elif message.data[0] == 3:
            sleep = 0.001
            limit = 1000
            direction = True
        elif message.data[0] == 4:
            sleep = 0.1
            limit = 10
            direction = False
        elif message.data[0] == 5:
            sleep = 0.01
            limit = 100
            direction = False
        elif message.data[0] == 6:
            sleep = 0.001
            limit = 1000
            direction = False
        else:
            time.sleep(1)
            continue

        dirpin.value = direction
        for i in range(0, limit):
            pin.value = True  # High (ON)
            time.sleep(sleep)
            pin.value = False
            time.sleep(sleep)


# Write your code here :-)

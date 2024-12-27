# Write your code here :-)
import board
import busio
import digitalio
import adafruit_mcp2515
import time

# Set up SPI and Chip Select (CS) pin
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CAN_CS)  # Update with correct CS pin

# Initialize MCP2515 with 100 kbps speed
can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)

# Set up the step and enable pins on the MCP2515 board
step = digitalio.DigitalInOut(board.D9)
direction = digitalio.DigitalInOut(board.D6)
step.direction = digitalio.Direction.OUTPUT
direction.direction = digitalio.Direction.OUTPUT

# Enable the stepper motor
direction.value = False


# Function to send a CAN message
def send_ready_message():
    ready_data = bytes([0x01])
    ready_message = adafruit_mcp2515.Message(id=0x321, data=ready_data, extended=False)
    can.send(ready_message)
    print("Sent 'Ready' message to Raspberry Pi")

# Function to step motor
def step_motor(steps, delay):
    for x in range(steps):
        print("Stepping forward")
        step.value = True
        time.sleep(delay)
        step.value = False
        time.sleep(delay)

# Send the "ready" message to the Raspberry Pi
send_ready_message()

print("Listening for CAN messages to control stepper...")

run = True

while run:
    message = can.read_message()  # Read incoming CAN message
    if message is not None:  # If a message is received
        print(f"Received message: ID={hex(message.id)}, Data={message.data}")
        step_motor(200, 1)
        run = False

    time.sleep(0.1)  # Small delay to prevent excessive CPU usage

# Write your code here :-)

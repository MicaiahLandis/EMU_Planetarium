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

# Set up the LED pin on the MCP2515 board
led = pwmio.PWMOut(board.D5, frequency=5000, duty_cycle=0)

# Function to send a CAN message
def send_ready_message():
    ready_data = bytes([0x01])
    ready_message = adafruit_mcp2515.Message(id=0x321, data=ready_data, extended=False)
    can.send(ready_message)
    print("Sent 'Ready' message to Raspberry Pi")

# Send the "ready" message to the Raspberry Pi
send_ready_message()

print("Listening for CAN messages to control LED...")

# Main loop
while True:
    message = can.read_message()  # Read incoming CAN message
    if message is not None:  # If a message is received
        print(f"Received message: ID={hex(message.id)}, Data={message.data[0]}")

        led.duty_cycle = message.data[0] * 250

    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
# Write your code here :-)

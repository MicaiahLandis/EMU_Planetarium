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

# Set up the LED pin on the MCP2515 board
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


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
        print(f"Received message: ID={hex(message.id)}, Data={message.data}")

        # Check if the message is intended for LED control
        if message.id == 0x123:  # Match the ID
            if message.data[0] == 0x01:  # Turn the LED on
                led.value = True
                print("LED ON")
            elif message.data[0] == 0x00:  # Turn the LED off
                led.value = False
                print("LED OFF")

    time.sleep(0.1)  # Small delay to prevent excessive CPU usage


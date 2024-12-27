# Write your code here :-)
import time
import board
import digitalio

# List of GPIO pins on Adafruit Feather RP2040
pins = [
    board.D5, board.D6, board.D9, board.D10, board.D11, board.D12, board.D13,  # Available GPIO pins
    board.A0, board.A1, board.A2, board.A3, board.D24, board.D25, board.D4,  # Analog pins as GPIO
    board.SCL, board.SDA, board.RX, board.TX, board.SCK, board.MOSI, board.MISO,
]

# Create a list of digitalio pin objects, set as outputs
pin_objects = []

for pin in pins:
    gpio = digitalio.DigitalInOut(pin)
    gpio.direction = digitalio.Direction.OUTPUT
    pin_objects.append(gpio)

# Main loop: Toggle each pin on and off every 3 seconds
while True:
    print("Turning ON all pins...")
    for gpio in pin_objects:
        gpio.value = True  # Turn pin ON

    time.sleep(3)  # Wait 3 seconds

    print("Turning OFF all pins...")
    for gpio in pin_objects:
        gpio.value = False  # Turn pin OFF

    time.sleep(3)  # Wait 3 seconds

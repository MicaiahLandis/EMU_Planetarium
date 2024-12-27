import board
import digitalio
import time
from canbus import canbus

# Set up a GPIO pin (D13 is the onboard LED, but you can change it)
pin = digitalio.DigitalInOut(board.D10)
pin.direction = digitalio.Direction.OUTPUT  # Configure as output

# The code you want to loop
def receiver_function(message):

    pin.value = True  # High (ON)
    time.sleep(0.001)
    pin.value = False
    time.sleep(0.001)


# Pass the function to the canbus
canbus(receiver_function)
# Write your code here :-)

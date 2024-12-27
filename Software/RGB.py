import time
import board
import neopixel

# Set up the NeoPixel (1 LED, connected to D6 for example)
pixel_pin = board.D6  # Change if connected to a different pin
num_pixels = 1

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# RGB color definitions
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (255, 255, 255)  # White
]

# Main loop to cycle through colors
while True:
    for color in colors:
        print(f"Setting color: {color}")
        pixel.fill(color)  # Set all pixels to the same color
        time.sleep(1)  # Wait 1 second before changing color

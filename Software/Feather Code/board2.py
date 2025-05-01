# Feather Board 2 (Axis 2: Latitude)
# EMU Engineering Capstone 2024-25
# Laura Benner
# laurabennerr@gmail.com

# Imports
import board
import digitalio
import time
import pwmio
import busio
import adafruit_mcp2515
import struct

# Constants
axis_id = 2
duty_cycle = 55000
steps = 9142 / 360

# State variables
calibrated = False
position = None
continuous_start_time = None
continuous_direction = None
continuous_speed = None
continuous_active = False

# Pin setup
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CAN_CS)
can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)
step_pin = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=200, variable_frequency=True)
direction_pin = digitalio.DigitalInOut(board.D13)
direction_pin.direction = digitalio.Direction.OUTPUT

# Move for a fixed duration
def timed(direction, speed, duration):
    global calibrated, position
    duration = int.from_bytes(duration, "big")
    direction_pin.value = direction
    step_pin.frequency = speed
    step_pin.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin.duty_cycle = 0
    if calibrated and direction:
        position = (position + (speed * duration / steps)) % 360
    elif calibrated:
        position = (position - (speed * duration / steps)) % 360

# Return to position 0
def calibrate(direction, speed, var):
    global calibrated, position
    direction_pin.value = direction
    step_pin.frequency = speed
    step_pin.duty_cycle = duty_cycle
    while True:
        message = can.read_message()
        if message is not None and message.data[0] == axis_id and message.data[1] == 4:
            break
    step_pin.duty_cycle = 0
    calibrated = True
    position = 0

# Move to specified coordinate (0-359)
def coordinate(direction, speed, coordinate):
    global position
    coordinate = struct.unpack("<f", bytes(coordinate))[0]
    direction = (coordinate - position) % 360 < (position - coordinate) % 360
    distance = min((coordinate - position) % 360, (position - coordinate) % 360)
    duration = distance * steps / speed
    direction_pin.value = direction
    step_pin.frequency = speed
    step_pin.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin.duty_cycle = 0
    position = coordinate

# Start/stop motion
def continuous(direction, speed, go):
    global continuous_start_time, continuous_direction, continuous_speed, continuous_active
    go = int.from_bytes(go, "big")
    if go:
        if continuous_active:
            update_position_from_elapsed()
        else:
            step_pin.duty_cycle = duty_cycle
            continuous_active = True
        continuous_direction = direction
        continuous_speed = speed
        direction_pin.value = direction
        step_pin.frequency = speed
        continuous_start_time = time.monotonic()
    else:
        if continuous_active:
            update_position_from_elapsed()
            step_pin.duty_cycle = 0
            continuous_active = False
            continuous_start_time = None

def update_position_from_elapsed():
    global position, continuous_start_time, continuous_direction, continuous_speed
    if calibrated and continuous_start_time is not None:
        elapsed = time.monotonic() - continuous_start_time
        delta = (continuous_speed * elapsed / steps) % 360
        if continuous_direction:
            position = (position + delta) % 360
        else:
            position = (position - delta) % 360

# Maps
function_map = {1: timed, 2: coordinate, 3: continuous, 4: calibrate}

direction_map = {0: False, 1: True}

speed_map = {0: 10, 1: 15, 2: 25}

# Check for CAN messages and execute appropriate function call
while True:
    message = can.read_message()
    if message is not None:
        if message.data[0] == axis_id or message.data[0] == 5:
            function_to_call = function_map.get(message.data[1])
            function_to_call(
                direction_map.get(message.data[2]),
                speed_map.get(message.data[3]),
                message.data[4:]
            )

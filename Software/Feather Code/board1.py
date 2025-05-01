# Feather Board 1 (Axis 1: Daily; Axis 4: Starball)
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
from adafruit_mcp2515.canio import Message
import struct

# Constants
axis_id_a = 1
axis_id_b = 4
duty_cycle = 55000
steps_a = 4571 / 360
steps_b = 2000 / 360

# State variables
calibrated_a = False
position_a = None
continuous_start_time_a = None
continuous_direction_a = None
continuous_speed_a = None
continuous_active_a = False
calibrated_b = False
position_b = None
continuous_start_time_b = None
continuous_direction_b = None
continuous_speed_b = None
continuous_active_b = False
calibrated_c = False

# Pin setup
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CAN_CS)
can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)
step_pin_a = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=200, variable_frequency=True)
direction_pin_a = digitalio.DigitalInOut(board.D13)
direction_pin_a.direction = digitalio.Direction.OUTPUT
step_pin_b = pwmio.PWMOut(board.D9, duty_cycle=0, frequency=200, variable_frequency=True)
direction_pin_b = digitalio.DigitalInOut(board.D10)
direction_pin_b.direction = digitalio.Direction.OUTPUT
ir_a = digitalio.DigitalInOut(board.SDA)
ir_a.direction = digitalio.Direction.INPUT
ir_a.pull = digitalio.Pull.UP
ir_b = digitalio.DigitalInOut(board.SCL)
ir_b.direction = digitalio.Direction.INPUT
ir_b.pull = digitalio.Pull.UP
ir_c = digitalio.DigitalInOut(board.D5)
ir_c.direction = digitalio.Direction.INPUT
ir_c.pull = digitalio.Pull.UP

# Move Axis 1 for a fixed duration
def timed_a(direction, speed, duration):
    global calibrated_a, position_a
    duration = int.from_bytes(duration, "big")
    direction_pin_a.value = direction
    step_pin_a.frequency = speed
    step_pin_a.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin_a.duty_cycle = 0
    if calibrated_a and direction:
        position_a = (position_a + (speed * duration / steps_a)) % 360
    elif calibrated_a:
        position_a = (position_a - (speed * duration / steps_a)) % 360

# Move Axis 4 for a fixed duration
def timed_b(direction, speed, duration):
    global calibrated_b, position_b
    duration = int.from_bytes(duration, "big")
    direction_pin_b.value = direction
    step_pin_b.frequency = speed
    step_pin_b.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin_b.duty_cycle = 0
    if calibrated_b and direction:
        position_b = (position_b + (speed * duration / steps_b)) % 360
    elif calibrated_b:
        position_b = (position_b - (speed * duration / steps_b)) % 360

# Return Axes to position 0
def calibrate(direction, speed, var):
    global calibrated_a, position_a, calibrated_b, position_b, calibrated_c
    calibrated_a = calibrated_b = calibrated_c = False
    
    # Start Daily Motion
    direction_pin_a.value = direction
    step_pin_a.frequency = speed
    step_pin_a.duty_cycle = duty_cycle

    # Start Starball
    direction_pin_b.value = direction
    step_pin_b.frequency = speed
    step_pin_b.duty_cycle = duty_cycle

    while True:
        if ir_a.value and not calibrated_a:
            step_pin_a.duty_cycle = 0
            calibrated_a = True
            position_a = 0
        if ir_b.value and not calibrated_b:
            step_pin_b.duty_cycle = 0
            calibrated_b = True
            position_b = 0
        if not ir_c.value and not calibrated_c:
            msg = Message(id=0x100, data=bytes([2, 4, 0, 0, 0]), extended=False) # Send CAN message to Board 2 to stop latitude axis
            can.send(msg)
            calibrated_c = True
        if calibrated_a and calibrated_b and calibrated_c:
            msg = Message(id=0x100, data=bytes([0]), extended=False) # Send CAN message to Raspberry Pi indicating finished calibration
            can.send(msg)
            break
        time.sleep(0.05)

# Move Axis 1 to specified coordinate (0-359)
def coordinate_a(direction, speed, coordinate):
    global position_a
    coordinate = struct.unpack("<f", bytes(coordinate))[0]
    direction = (coordinate - position_a) % 360 < (position_a - coordinate) % 360
    distance = min((coordinate - position_a) % 360, (position_a - coordinate) % 360)
    duration = distance * steps_a / speed
    direction_pin_a.value = direction
    step_pin_a.frequency = speed
    step_pin_a.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin_a.duty_cycle = 0
    position_a = coordinate

# Move Axis 4 to specified coordinate (0-359)
def coordinate_b(direction, speed, coordinate):
    global position_b
    coordinate = struct.unpack("<f", bytes(coordinate))[0]
    direction = (coordinate - position_b) % 360 < (position_b - coordinate) % 360
    distance = min((coordinate - position_b) % 360, (position_b - coordinate) % 360)
    duration = distance * steps_b / speed
    direction_pin_b.value = direction
    step_pin_b.frequency = speed
    step_pin_b.duty_cycle = duty_cycle
    time.sleep(duration)
    step_pin_b.duty_cycle = 0
    position_b = coordinate

# Start/stop motion of Axis 1
def continuous_a(direction, speed, go):
    global continuous_start_time_a, continuous_direction_a, continuous_speed_a, continuous_active_a
    go = int.from_bytes(go, "big")
    if go:
        if continuous_active_a:
            update_position_from_elapsed_a()
        else:
            step_pin_a.duty_cycle = duty_cycle
            continuous_active_a = True
        continuous_direction_a = direction
        continuous_speed_a = speed
        direction_pin_a.value = direction
        step_pin_a.frequency = speed
        continuous_start_time_a = time.monotonic()
    else:
        if continuous_active_a:
            update_position_from_elapsed_a()
            step_pin_a.duty_cycle = 0
            continuous_active_a = False
            continuous_start_time_a = None

# Start/stop motion of Axis 4
def continuous_b(direction, speed, go):
    global continuous_start_time_b, continuous_direction_b, continuous_speed_b, continuous_active_b
    go = int.from_bytes(go, "big")
    if go:
        if continuous_active_b:
            update_position_from_elapsed_b()
        else:
            step_pin_b.duty_cycle = duty_cycle
            continuous_active_b = True
        continuous_direction_b = direction
        continuous_speed_b = speed
        direction_pin_b.value = direction
        step_pin_b.frequency = speed
        continuous_start_time_b = time.monotonic()
    else:
        if continuous_active_b:
            update_position_from_elapsed_b()
            step_pin_b.duty_cycle = 0
            continuous_active_b = False
            continuous_start_time_b = None

def do_nothing(*args):
    pass

def update_position_from_elapsed_a():
    global position_a, continuous_start_time_a, continuous_direction_a, continuous_speed_a
    if calibrated_a and continuous_start_time_a is not None:
        elapsed = time.monotonic() - continuous_start_time_a
        delta = (continuous_speed_a * elapsed / steps_a) % 360
        if continuous_direction_a:
            position_a = (position_a + delta) % 360
        else:
            position_a = (position_a - delta) % 360

def update_position_from_elapsed_b():
    global position_b, continuous_start_time_b, continuous_direction_b, continuous_speed_b
    if calibrated_b and continuous_start_time_b is not None:
        elapsed = time.monotonic() - continuous_start_time_b
        delta = (continuous_speed_b * elapsed / steps_b) % 360
        if continuous_direction_b:
            position_b = (position_b + delta) % 360
        else:
            position_b = (position_b - delta) % 360

# Maps
function_map = {1: timed_a, 2: coordinate_a, 3: continuous_a, 4: calibrate, 5: timed_b, 6: coordinate_b, 7: continuous_b, 8: do_nothing}
direction_map = {0: False, 1: True}

speed_map = {0: 25, 1: 50, 2: 100}

# Check for CAN messages and execute appropriate function call
while True:
    message = can.read_message()
    if message is not None:
        print(message.data)
        if message.data[0] == axis_id_a or message.data[0] == 5:
            function_to_call = function_map.get(message.data[1])
            function_to_call(
                direction_map.get(message.data[2]),
                speed_map.get(message.data[3]),
                message.data[4:]
            )
        if message.data[0] == axis_id_b or message.data[0] == 5:
            function_to_call = function_map.get(message.data[1]+4)
            function_to_call(
                direction_map.get(message.data[2]),
                speed_map.get(message.data[3]),
                message.data[4:]
            )

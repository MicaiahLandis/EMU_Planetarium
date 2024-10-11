import os
import can

# Set up CAN interface with bitrate
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

# Create a CAN bus interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Construct the CAN message
# arbitration_id: identifier for the CAN message
# data: list of bytes to send, e.g., up to 8 bytes for CAN standard
message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04], is_extended_id=False)

# Send the CAN message
try:
    bus.send(message)
    print("Message sent")
except can.CanError:
    print("Message NOT sent")

# Bring down the CAN interface
os.system('sudo ifconfig can0 down')

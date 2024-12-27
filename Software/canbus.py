def canbus(receiver_function):
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
    can = adafruit_mcp2515.MCP2515(spi, cs, baudrate=100000)# Write your code here :-)

    # Function to send a CAN message
    def send_ready_message():
        ready_data = bytes([0x01])
        ready_message = adafruit_mcp2515.Message(id=0x321, data=ready_data, extended=False)
        can.send(ready_message)
        print("Sent 'Ready' message to Raspberry Pi")

    # Send the "ready" message to the Raspberry Pi
    send_ready_message()

    print("Listening for CAN messages...")

    # Main loop
    while True:
        message = can.read_message()  # Read incoming CAN message
        if message is not None:  # If a message is received
            receiver_function(message.data[0])
            print('message')

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    # Write your code here :-)

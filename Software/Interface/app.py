"""
Laura Benner
laurabennerr@gmail.com
EMU Engineering Capstone 2024-25
"""

# Imports
from flask import Flask, request, jsonify, render_template # type: ignore
import can # type: ignore
import signal
import sys
import os
import struct
from gpiozero import LED # type: ignore
from datetime import datetime
import pytz # type: ignore
from timezonefinder import TimezoneFinder # type: ignore
from astropy.time import Time # type: ignore
from astropy.coordinates import EarthLocation # type: ignore
import astropy.units as u # type: ignore

app = Flask(__name__)

# Render app
@app.route('/')
def home():
    return render_template('index.html')


# ---- CAN BUS ----

# CAN bus up
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Shut down CAN bus on exit
def shutdown_can_bus(signal, frame):
    os.system('sudo ifconfig can0 down')
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_can_bus)
signal.signal(signal.SIGTERM, shutdown_can_bus)

# Send message via CAN bus
def send_can_message(data):
    message = can.Message(arbitration_id=0x100, data=data, is_extended_id=False)
    bus.send(message)


# ---- CALIBRATION ----

# Global calibration status
calibrated = False

# Calibrate
def perform_calibration():
    global calibrated
    
    send_can_message([5, 4, 0, 1, 0, 0])

    calibrated_count = 0
    while True:
        msg = bus.recv(timeout=1.0)
        if msg and msg.data[0] == 0:
            if calibrated_count == 1:
                break
            else:
                calibrated_count = 1

    calibrated = True

@app.route('/calibrate', methods=['POST'])
def calibrate():
    perform_calibration()
    return '', 204


# ---- CONTINUOUS MOTION ----

# Update motion
@app.route('/update_motion', methods=['POST'])
def update_motion():
    data = request.json
    axis = data.get('axis')
    function = 3
    direction = {"forward": 1, "backward": 0}.get(data.get('direction'))
    speed = {"slow": 0, "medium": 1, "fast": 2}.get(data.get('speed'), 0)
    extra = int(data.get('extra'))
    extra_low = extra & 0xFF
    extra_high = (extra >> 8) & 0xFF

    send_can_message([axis, function, direction, speed, extra_high, extra_low])
    return '', 204


# ---- SKY SIMULATOR ----

# Simulate sky
@app.route('/sky_simulator', methods=['POST'])
def sky_simulator():
    data = request.json
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    date = data.get('date')
    time = data.get('time')

    tz = pytz.timezone(TimezoneFinder().timezone_at(lat=latitude, lng=longitude))
    utc = tz.localize(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")).astimezone(pytz.utc)
    t = Time(utc)
    loc = EarthLocation(lat=float(latitude)*u.deg, lon=float(longitude)*u.deg)
    sidereal = t.sidereal_time('apparent', longitude=loc.lon).deg

    # Stop continuous motion of all axes
    send_can_message([5, 3, 0, 0, 0, 0])

    # Calibrate if not already
    if not calibrated:
        perform_calibration()
        
    latitude_coord = 90 - latitude
    daily_coord = (sidereal+85.15) % 360
    precession_coord = 348

    send_can_message([2, 2, 0, 1]+list(struct.pack('<f', latitude_coord)))
    send_can_message([1, 2, 0, 1]+list(struct.pack('<f', daily_coord)))
    send_can_message([4, 2, 0, 1]+list(struct.pack('<f', precession_coord)))

    return '', 204


# ---- LIGHTS ----

# Global light dictionary
lights = {}

@app.route('/toggle-light', methods=['POST'])
def toggle_light():
    global lights

    data = request.get_json()
    pins = data.get('pins')

    for pin in pins:
        if pin not in lights:
            lights[pin] = LED(pin=pin, active_high=False)

        lights[pin].toggle()

    return '', 204


# ---- SHOW ----

@app.route('/show/<int:index>', methods=['POST'])
def show(index):
    if index == 1:
        if not calibrated:
            perform_calibration()
        if 26 not in lights:
            lights[26] = LED(pin=26, active_high=False)
        lights[26].toggle()
        if 7 not in lights:
            lights[7] = LED(pin=7, active_high=False)
        lights[7].toggle()
        send_can_message([4, 2, 0, 1]+list(struct.pack('<f', 348)))
        send_can_message([3, 2, 0, 1]+list(struct.pack('<f', 135)))
    elif index == 2:
        send_can_message([1, 2, 0, 1]+list(struct.pack('<f', 232)))
        send_can_message([2, 2, 0, 1]+list(struct.pack('<f', 51.5)))
    elif index == 3:
        if 3 not in lights:
            lights[3] = LED(pin=3, active_high=False)
        lights[3].toggle()
    elif index == 4:
        lights[3].toggle()
    elif index == 5:
        send_can_message([3, 2, 0, 1]+list(struct.pack('<f', 15)))
    elif index == 6:
        if 12 not in lights:
            lights[12] = LED(pin=12, active_high=False)
        lights[12].toggle()
    elif index == 7:
        lights[12].toggle()
        send_can_message([1, 2, 0, 1]+list(struct.pack('<f', 320)))
        send_can_message([3, 2, 0, 1]+list(struct.pack('<f', 195)))
        send_can_message([4, 2, 0, 1]+list(struct.pack('<f', 279)))
    elif index == 8:
        if 19 not in lights:
            lights[19] = LED(pin=19, active_high=False)
        lights[19].toggle()
        if 27 not in lights:
            lights[27] = LED(pin=27, active_high=False)
        lights[27].toggle()
    elif index == 9:
        lights[27].toggle()
        send_can_message([3, 2, 0, 1]+list(struct.pack('<f', 300)))
    elif index == 10:
        lights[19].toggle()
    elif index == 11:
        send_can_message([3, 2, 0, 1]+list(struct.pack('<f', 15)))
        lights[12].toggle()
    elif index == 12:
        lights[12].toggle()
    elif index == 13:
        lights[7].toggle()
        lights[26].toggle()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

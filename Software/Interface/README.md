# Planetarium Interface

## Setup
Edit the Raspberry Pi config file:

```bash
sudo nano /boot/firmware/config.txt
```

Add the following lines at the bottom to set up CAN bus and set the relays to be off by default:
```bash
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
dtoverlay=spi0-1cs

gpio=2=op,dh
gpio=3=op,dh
gpio=17=op,dh
gpio=18=op,dh
gpio=27=op,dh
gpio=22=op,dh
gpio=23=op,dh
gpio=24=op,dh
gpio=7=op,dh
gpio=5=op,dh
gpio=6=op,dh
gpio=12=op,dh
gpio=13=op,dh
gpio=19=op,dh
gpio=16=op,dh
gpio=26=op,dh
```

Navigate to your project directory.
```bash
pip install flask can pytz timezonefinder astropy
python -m venv venv
```

## Usage
```bash
source venv/bin/activate
python app.py
```

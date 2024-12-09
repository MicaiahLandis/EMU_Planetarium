from astropy.coordinates import SkyCoord
import time

def initialize_alignment_to_polaris(motor_ra, motor_dec):
    """
    Initialize the planetarium system to align with Polaris (North Star).
    
    Parameters:
    - motor_ra: function to move the RA motor to a specified position (degrees)
    - motor_dec: function to move the Dec motor to a specified position (degrees)
    
    Returns:
    - dict confirming alignment with Polaris (RA and Dec positions).
    """
    # Define Polaris coordinates
    polaris_ra = 37.95456067  # Right Ascension in degrees
    polaris_dec = 89.26410897  # Declination in degrees
    polaris = SkyCoord(ra=polaris_ra, dec=polaris_dec, unit='deg', frame='icrs')

    # Align motors to Polaris' RA and Dec
    print("Initializing alignment to Polaris...")
    motor_ra(polaris.ra.degree)
    motor_dec(polaris.dec.degree)

    # Confirm alignment
    print(f"Alignment complete: RA={polaris.ra.degree}°, Dec={polaris.dec.degree}°")
    return {"RA (degrees)": polaris.ra.degree, "Dec (degrees)": polaris.dec.degree}

# Mock motor functions for demonstration
def mock_motor_ra(target_ra):
    print(f"Moving RA motor to {target_ra} degrees...")
    time.sleep(1)  # Simulate motor movement delay

def mock_motor_dec(target_dec):
    print(f"Moving Dec motor to {target_dec} degrees...")
    time.sleep(1)  # Simulate motor movement delay

# Example usage
if __name__ == "__main__":
    alignment = initialize_alignment_to_polaris(mock_motor_ra, mock_motor_dec)
    print("System aligned to Polaris:", alignment)


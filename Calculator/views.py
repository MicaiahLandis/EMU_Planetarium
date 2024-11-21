from django.shortcuts import render
from django.http import HttpResponse
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_sun
import astropy.units as u

def index(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Combine date and time into a single datetime object
        datetime_str = f"{date}T{time}"
        t = Time(datetime_str, format='isot', scale='utc')

        # Create EarthLocation object
        location = EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg)

        # Calculate sidereal time
        sidereal = t.sidereal_time('mean', longitude=location)

        # Calculate target right ascension and declination (example: Sun)
        sun = get_sun(t)
        target_ra = sun.ra
        target_dec = sun.dec

        context = {
            'sidereal': sidereal,
            'target_ra': target_ra,
            'target_dec': target_dec,
        }
        return render(request, 'results.html', context)

    return render(request, 'input_form.html')

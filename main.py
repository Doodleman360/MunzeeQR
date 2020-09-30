import time
import board
import busio
import adafruit_gps
import serial
import qrcode
from papirus import PapirusTextPos

uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)
text = PapirusTextPos(False)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)

#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz)
gps.send_command(b"PMTK220,1000")

# Main loop
last_print = time.monotonic()
text.AddText("Waiting", Id="Top")
text.AddText("Sat:", 0, 20, Id="Sat")
text.AddText("Alt:", 0, 40, Id="Alt")
text.AddText("Speed:", 0, 60, Id="Speed")
text.WriteAll()
waiting = True
while True:
    gps.update()
    # Every 5 seconds print out current location details if there's a fix.
    current = time.monotonic()
    if (current - last_print >= 10.0):
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            if waiting is False:
                text.UpdateText("Top", "Waiting for fix...")
                text.WriteAll()
                waiting = True
            continue
        text.UpdateText("Top", "We have a fix!")
        waiting = False
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print("=" * 40)  # Print a separator line.
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,
            )
        )
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        print("Fix quality: {}".format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print("# satellites: {}".format(gps.satellites))
            text.UpdateText("Sat", "Sat: {}".format(gps.satellites))
        else:
            text.UpdateText("Sat", "Sat: 0")

        if gps.altitude_m is not None:
            print("Altitude: {} meters".format(gps.altitude_m))
            text.UpdateText("Alt", "Alt: {}".format(gps.altitude_m))
        else:
            text.UpdateText("Alt", "Alt: N/A")

        if gps.speed_knots is not None:
            print("Speed: {} knots".format(gps.speed_knots))
            text.UpdateText("Speed", "Speed: {}".format(gps.speed_knots))
        else:
            text.UpdateText("Speed", "Speed: 0")

        if gps.track_angle_deg is not None:
            print("Track angle: {} degrees".format(gps.track_angle_deg))

        if gps.horizontal_dilution is not None:
            print("Horizontal dilution: {}".format(gps.horizontal_dilution))

        if gps.height_geoid is not None:
            print("Height geo ID: {} meters".format(gps.height_geoid))

        text.WriteAll()

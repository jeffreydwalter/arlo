from Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

	# Get the list of devices and filter on device type to only get the basestation.
	# This will return an array which includes all of the basestation's associated metadata.
	basestations = arlo.GetDevices('basestation')

        # Get the list of devices and filter on device type to only get the camera.
        # This will return an array which includes all of the camera's associated metadata.
        cameras = arlo.GetDevices('camera')

        # Turn temperature alerts on
        arlo.TempAlertOn(cameras[0])

        # Alert min threshold (so if temp falls below this number it alerts)
        arlo.TempAlertThresholdMin(cameras[0], 170)

        # Alert max threshold (so if temp go above this number it alerts)
        arlo.TempAlertThresholdMax(cameras[0], 270)

        # record temperature history
        arlo.TempRecordingOn(cameras[0])

        # Set the temperature unit to Celcius
        arlo.SetTempUnit(cameras[0]["uniqueId"], "C")

except Exception as e:
    print(e)

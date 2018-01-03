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

	# Set camera brightness to 0%.
	#arlo.AdjustBrightness(basestations[0], cameras[0] -2)

	# Set camera brightness to 25%.
	#arlo.AdjustBrightness(basestations[0], cameras[0], -1)

	# Set camera brightness to 50%.
	arlo.AdjustBrightness(basestations[0], cameras[0], 0)

	# Set camera brightness to 75%.
	#arlo.AdjustBrightness(basestations[0], cameras[0], 1)

	# Set camera brightness to 100%.
	#arlo.AdjustBrightness(basestations[0], cameras[0], 2)

except Exception as e:
    print(e)

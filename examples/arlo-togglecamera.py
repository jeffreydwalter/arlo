from arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

        # Get the list of devices and filter on device type to only get the basestations.
	# This will return an array of basestations, including all of the basestations' associated metadata.
        basestations = arlo.GetDevices('basestation')
	
        # Get the list of devices and filter on device type to only get the cameras.
	# This will return an array of cameras, including all of the cameras' associated metadata.
	cameras = arlo.GetDevices('camera')

	# Turn camera on.
	print(arlo.ToggleCamera(basestations[0], cameras[0], True))
	# Turn camera off.
	#print(arlo.ToggleCamera(basestations[0], cameras[0], False))

except Exception as e:
    print(e)

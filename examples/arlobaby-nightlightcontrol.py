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

        # Get current state payload
        state=arlo.GetCameraState(cameras[0])
        print(state["properties"][0]["nightLight"])

        # night light on
        arlo.SetNightLightOn(cameras[0])

        # night light timer on
        arlo.SetNightLightTimerOn(cameras[0], 500)
	
	# night light color mode
	arlo.SetNightLightMode(cameras[0], mode={"blue":255,"green":255,"red":255 }) # or mode="rainbow"

except Exception as e:
    print(e)

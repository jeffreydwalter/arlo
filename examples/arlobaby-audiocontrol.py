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
        arlo.GetAudioPlayback(cameras[0])

        # Start playing
        arlo.PlayTrack(cameras[0], track_id, position)

        # Pause the track
        arlo.PauseTrack(cameras[0])

        # Skip the track
        arlo.SkipTrack(cameras[0])

        # Set the sleep timer
        arlo.SetSleepTimerOn(cameras[0])

        # Set the playback mode ot continuous
        arlo.SetLoopBackModeContinuous(cameras[0])

except Exception as e:
    print(e)

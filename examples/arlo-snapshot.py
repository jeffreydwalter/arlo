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
    
    # Get the list of devices and filter on device type to only get the cameras.
    # This will return an array of cameras, including all of the cameras' associated metadata.
    cameras = arlo.GetDevices('camera')

    # Starting recording with a camera.
    arlo.StartRecording(cameras[0]);

    # Wait for 4 seconds while the camera records. (There are probably better ways to do this, but you get the idea.)
    time.sleep(4)

    # Trigger the snapshot.
    arlo.TriggerStreamSnapshot(basestations[0], cameras[0]);
    
    # Stop recording.
    arlo.StopRecording(cameras[0]);

except Exception as e:
    print(e):

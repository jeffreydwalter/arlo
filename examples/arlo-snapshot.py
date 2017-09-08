from Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.
 
    # Filter on device type to only get the cameras.
    # This will return an array which includes all of the cameras and their associated metadata.
    cameras = arlo.GetDevices('camera')

    # Starting recording with a camera.
    arlo.StartRecording(cameras[0])

    # Wait for 4 seconds while the camera records. (There are probably better ways to do this, but you get the idea.)
    time.sleep(4)

    # Stop recording.
    arlo.StopRecording(cameras[0])

    # Take the snapshot.
    arlo.TakeSnapshot(cameras[0])

except Exception as e:
    print (e)

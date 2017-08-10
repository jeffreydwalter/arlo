from Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    # Get the list of devices.
    devices = arlo.GetDevices()

    # Filter on device type to only get the basestation.
    # This will return an array which includes all of the basestation's associated metadata.
    basestation = [ device for device in devices if device['deviceType'] == 'basestation' ]

    # Filter on device type to only get the cameras.
    # This will return an array which includes all of the cameras and their associated metadata.
    cameras = [ device for device in devices if device['deviceType'] == 'camera' ]

    # Starting recording with a camera.
    arlo.StartRecording(basestation[0]['deviceId'], cameras[0]['deviceId'], basestation[0]['xCloudId'], cameras[0]['properties']['olsonTimeZone']);

    # Wait for 4 seconds while the camera records. (There are probably better ways to do this, but you get the idea.)
    time.sleep(4)

    # Stop recording.
    arlo.StopRecording(basestation[0]['deviceId'], cameras[0]['deviceId'], basestation[0]['xCloudId'], cameras[0]['properties']['olsonTimeZone']);

    # Take the snapshot.
    arlo.TakeSnapshot(basestation[0]['deviceId'], cameras[0]['deviceId'], basestation[0]['xCloudId'], cameras[0]['properties']['olsonTimeZone']);

except Exception as e:
    print (e)

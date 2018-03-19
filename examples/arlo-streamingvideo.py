from Arlo import Arlo

from subprocess import call

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:

    # Instantiating the Arlo object automatically calls Login(),
    # which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    # Get the list of devices and filter on device type to only get the cameras.
    # This will return an array which includes all of the canera's associated metadata.
    cameras = arlo.GetDevices('camera')

    # Get the list of devices and filter on device type to only get the basestation.
    # This will return an array which includes all of the basestation's associated metadata.
    basestations = arlo.GetDevices('basestation')
    
    # Send the command to start the stream and return the stream url.
    url = arlo.StartStream(basestations[0], cameras[0])

    # Record the stream to a file named 'test.mp4'.
    # **Requires ffmpeg 3.4 or greater.**
    # For this example, I'm going to open ffmpeg.
    # Crucially important is the '-t' flag, which specifies a recording time. (See the ffmpeg documentation.)
    # This is just a crude example, but hopefully it will give you some ideas.
    # You can use any number of libraries to do the actual streaming. OpenCV or VLC are both good choices.
    # NOTE: This will print the output of ffmpeg to STDOUT/STDERR. If you don't want that, you will
    # need to pass additional arguments to handle those streams.

    call(['ffmpeg', '-re', '-i', url, '-t', '10', '-acodec', 'copy', '-vcodec', 'copy', 'test.mp4'])

except Exception as e:
    print(e)

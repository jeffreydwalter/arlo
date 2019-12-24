from arlo import Arlo

from datetime import timedelta, date
import datetime
import sys, os
sys.path.append('..')
#import json

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

videopath = 'videos'

try:
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    # Get the list of devices and filter on device type to only get the cameras.
    # This will return an array which includes all of the canera's associated metadata
    # and includes Arlo Q devices, re: https://github.com/jeffreydwalter/arlo/wiki/FAQ#frequently-asked-questions
    cameras = arlo.GetDevices('camera')
    arloq = arlo.GetDevices('arloq')
    arloqs = arlo.GetDevices('arloqs')

    cameras = cameras + arloq + arloqs
    cameras_by_id = {}

    # setup a hash where each camera deviceId is assocaited with its name for lookup later
    for camera in cameras:
        cameras_by_id[camera['deviceId']] = camera['deviceName']

    today = (date.today() - timedelta(days=0)).strftime("%Y%m%d")
    seven_days_ago = (date.today() - timedelta(days=7)).strftime("%Y%m%d")

    # Get all of the recordings for a date range.
    library = arlo.GetLibrary(seven_days_ago, today)

    # Check if videos folder already exists
    if not os.path.exists(videopath):
        os.makedirs(videopath)

    # Iterate through the recordings in the library.
    for recording in library:

        # Set the extension based on the content type of the returned media
        content_type = recording['contentType']
        extension = '.jpg' if content_type == 'image/jpg' else '.mp4'
        
        # Grab the camera name to use for the filename from the cameras_by_id hash above
        camera_name = cameras_by_id[recording['deviceId']]

        videofilename = camera_name + ' - ' + datetime.datetime.fromtimestamp(int(recording['name']) // 1000).strftime('%Y-%m-%d %H-%M-%S') + extension
        
        # Download the video and write it to the given path.
        arlo.DownloadRecording(recording['presignedContentUrl'], videopath + '/' + videofilename)

        print('Downloaded video ' + videofilename + ' from ' + recording['createdDate'] + '.')

        # Use the following line to print all the data we got for the recording.
        #print(json.dumps(recording, indent = 4))

    # Delete all of the videos you just downloaded from the Arlo library.
    # Notice that you can pass the "library" object we got back from the GetLibrary() call.
    #result = arlo.BatchDeleteRecordings(library)

    # If we made it here without an exception, then the videos were successfully deleted.
    #print ('Batch deletion of videos completed successfully.')

    arlo.Logout()
    print('Logged out')

except Exception as e:
    print(e)

import sys, os
sys.path.append('..')
import requests
from arlo import Arlo
from datetime import timedelta, date
import datetime
import json
import re

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

videopath = 'videos'
cameraNumber = 2
datetimeFrom = datetime.datetime.strptime('2018-08-11 03:00:00', '%Y-%m-%d %H:%M:%S');
datetimeTo = datetime.datetime.strptime('2018-08-11 04:00:00', '%Y-%m-%d %H:%M:%S');


try:
    print("Downloading cvr videos from " + datetimeFrom.strftime("%Y-%m-%d %H:%M:%S") + " to " + datetimeTo.strftime("%Y-%m-%d %H:%M:%S"))
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

    # Get all of the recordings for a date range.
    playlist = arlo.GetCvrPlaylist(cameras[cameraNumber], datetimeFrom.strftime("%Y%m%d"), datetimeTo.strftime("%Y%m%d"))

    # If no recordings are available exit
    if not playlist['playlist']:
        print("No playlist found for camera for the period " + datetimeFrom.strftime("%Y-%m-%d %H:%M:%S") + " and " + datetimeTo.strftime("%Y-%m-%d %H:%M:%S"))
        arlo.Logout()
        print('Logged out')
        sys.exit()


    # Check if videos folder already exists
    if not os.path.exists(videopath):
        os.makedirs(videopath)

    # debug to show the playlist json
    # print(json.dumps(playlist, indent = 4))

    # Iterate through each day in the cvr playlist.
    for playlistPerDay in playlist['playlist']:
        # Iterate through each m3u8 (playlist) file
        for recordings in playlist['playlist'][playlistPerDay]:
            m3u8 = requests.get(recordings['url']).text.split("\n")
            # Iterate the m3u8 file and get all the streams
            for m3u8Line in m3u8:
                # debug to show the m3u8 file
                # print m3u8Line

                # Split the url into parts used for filename (camera id and timestamp)
                m = re.match("^http.+([A-Z0-9]{13})_[0-9]{13}_([0-9]{13})", m3u8Line)
                if m:
                    cameraId = m.group(1)
                    videoTime = datetime.datetime.fromtimestamp(int(m.group(2)) // 1000)

                    # If we are within desired range, then download
                    if videoTime > datetimeFrom and videoTime < datetimeTo:
                        # Get video as a chunked stream; this function returns a generator.
                        stream = arlo.StreamRecording(m3u8Line)
                        videofilename = cameraId + '-' + videoTime.strftime('%Y%m%d-%H%M%S') + '.mp4'

                        # Skip files already downloaded
                        if os.path.isfile(videopath + '/' + videofilename):
                            print("Video " + videofilename + " already exists")
                        else:
                            print('Downloading video ' + videofilename)
                            with open(videopath + '/' + videofilename, 'wb') as f:
                                for chunk in stream:
                                    f.write(chunk)
                                f.close()

    arlo.Logout()
    print('Logged out')

except Exception as e:
    print(e)

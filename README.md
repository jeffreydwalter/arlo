# arlo ![](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg)
> Python module for interacting with Netgear's Arlo camera system.

This just a personal utility that I created out of necessity. It is by no means complete, although it does expose quite a bit of the Arlo interface in an easy to use Python pacakge.

As such, this package does not come with unit tests (feel free to add them) or guarantees.

*I'm not a Python developer by trade and I don't plan on doing much more work on this library outside of fixing any bugs I find or adding any APIs I discover I need.*

**Please, feel free to contribute to this repo or, buy Jeff a beer!** [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=R77B7UXMLA6ML&lc=US&item_name=Jeff%20Needs%20Beer&item_number=buyjeffabeer&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

To get started, just do:

```
$ git clone https://github.com/jeffreydwalter/arlo.git
```
**NOTE: arlo.netgear.com requires TLS 1.2 for their API. So, if you're getting ssl errors, it's most likely related to your version of openssl. You must upgrade your openssl library.
If you're running this library on OSX or macOS, they ship with openssl v0.9.x which does not support TLS 1.2. You should follow the instructions found here https://comeroutewithme.com/2016/03/13/python-osx-openssl-issue/ to upgrade your openssl library.**

Once you have the repository cloned, you can import and use it, like so:

```python
from datetime import timedelta, date
from Arlo import Arlo
import datetime

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

	today = (date.today()-timedelta(days=0)).strftime("%Y%m%d")
	seven_days_ago = (date.today()-timedelta(days=7)).strftime("%Y%m%d")

	# Get all of the recordings for a date range.
	library = arlo.GetLibrary(seven_days_ago, today)

	# Iterate through the recordings in the library.
	for recording in library:

		videofilename = datetime.datetime.fromtimestamp(int(recording['name'])//1000).strftime('%Y-%m-%d %H-%M-%S') + ' ' + recording['uniqueId'] + '.mp4'
		##
		# The videos produced by Arlo are pretty small, even in their longest, best quality settings,
		# but you should probably prefer the chunked stream (see below). 
		###    
		#    # Download the whole video into memory as a single chunk.
		#    video = arlo.GetRecording(recording['presignedContentUrl'])
		#	 with open('videos/'+videofilename, 'w') as f:
		#        f.write(stream)
		#        f.close()
		# Or:
		#
		# Get video as a chunked stream; this function returns a generator.
		stream = arlo.StreamRecording(recording['presignedContentUrl'])
		with open('videos/'+videofilename, 'w') as f:
			for chunk in stream:
				f.buffer.write(chunk)
			f.close()

		print ('Downloaded video '+videofilename+' from '+recording['createdDate']+'.')

	# Delete all of the videos you just downloaded from the Arlo library.
	# Notice that you can pass the "library" object we got back from the GetLibrary() call.
	result = arlo.BatchDeleteRecordings(library)

	# If we made it here without an exception, then the videos were successfully deleted.
	print ('Batch deletion of videos completed successfully.')

except Exception as e:
    print (e)
```

Here's an example of arming/disarming Arlo.

```python
from Arlo.Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

	# Get the list of devices and filter on device type to only get the basestation.
	# This will return an array which includes all of the basestation's associated metadata.
	basestation = [ device for device in arlo.GetDevices() if device['deviceType'] == 'basestation' ]

	# Arm Arlo.
	arlo.Arm(basestation[0]['deviceId'], basestation[0]['xCloudId'])
	# Or
	# Disarm Arlo.
	# arlo.Disarm(basestation[0]['deviceId'], basestation[0]['xCloudId'])

except Exception as e:
    print (e)
```

Here's an example of toggling an Arlo camera. 

```python
from Arlo.Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	arlo = Arlo(USERNAME, PASSWORD)

	# Get the list of devices and filter on device type to only get the cameras.
	# This will return an array of cameras, including all of the cameras' associated metadata.
	devices = [ device for device in arlo.GetDevices() if device['deviceType'] == 'camera']
	# Turn camera on.
	print (arlo.ToggleCamera(devices[0]['deviceId'], devices[0]['xCloudId'], True)))
	# Turn camera off.
	print (arlo.ToggleCamera(devices[0]['deviceId'], devices[0]['xCloudId'], False)))

except Exception as e:
    print (e)

```
## Todo:
- [x] LICENSE
- [x] README
- [x] First pass at Arlo API in Python 
- [x] Basic code example 
- [ ] Unit tests
- [ ] Add missing APIs
- [ ] Turn this into a proper pip package.
- [ ] Add better documentation
- [ ] Have a cold beer?

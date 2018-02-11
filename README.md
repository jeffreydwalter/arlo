# arlo ![](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg)
> Python module for interacting with Netgear's Arlo camera system.

This just a personal utility that I created out of necessity. It is by no means complete, although it does expose quite a bit of the Arlo interface in an easy to use Python pacakge. As such, this package does not come with unit tests (feel free to add them) or guarantees.
**All [contributions](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) are welcome and appreciated!**

**Please, feel free to [contribute](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) to this repo or buy Jeff a beer!** [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=R77B7UXMLA6ML&lc=US&item_name=Jeff%20Needs%20Beer&item_number=buyjeffabeer&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

---
### Generous Benefactors (Thank you!)
* [cubewot](https://github.com/cubewot) - 🍺🍺 
* [imopen](https://github.com/imopen) - 🍺 
* [notalifeform](https://github.com/notalifeform) - 🍺🍺
* []()anonymous - 🍺🍺🍺🍺 
---
### Awesomely Smart Contributors (Thank you!)
* [notalifeform](https://github.com/notalifeform) - Feb 10, 2018 - Fixed bug and formatting in example script.
* [erosen](https://github.com/erosen) - Jan 27, 2018 - Added the ArloQ camera schema to the wiki.
* [deanmcguire](https://github.com/deanmcguire) - Dec 7, 2017 - Unravelled the mysteries of RTSP streaming video.
* [andijakl](https://github.com/andijakl) - Jul 24, 2017 - Added Python 3 support and cleaned up examples.
* [cemeyer2](https://github.com/cemeyer2) - Nov 26, 2016 - Fixed setup issues.
* [LenShustek](https://github.com/LenShustek) - Sep 14, 2016, - Added Logout().

If You'd like to make a diffrence in the world and get your name on this most prestegious list, have a look at our [help wanted](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) section!

---

## Install
```bash
$ pip install arlo

# Install from master branch
$ pip install git+https://github.com/jeffreydwalter/arlo
```

**NOTE: arlo.netgear.com requires TLS 1.2 for their API. So, if you're getting ssl errors, it's most likely related to your version of openssl. You must upgrade your openssl library.
If you're running this library on OSX or macOS, they ship with openssl v0.9.x which does not support TLS 1.2. You should follow the instructions found here https://comeroutewithme.com/2016/03/13/python-osx-openssl-issue/ to upgrade your openssl library.**

After installing all of the required libraries, you can import and use this library like so:

```python
from Arlo import Arlo

from datetime import timedelta, date
import datetime
import sys

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
		#	 with open('videos/'+videofilename, 'wb') as f:
		#        f.write(stream)
		#        f.close()
		# Or:
		#
		# Get video as a chunked stream; this function returns a generator.
		stream = arlo.StreamRecording(recording['presignedContentUrl'])
		with open('videos/'+videofilename, 'wb') as f:
			for chunk in stream:
				f.write(chunk)
			f.close()

		print('Downloaded video '+videofilename+' from '+recording['createdDate']+'.')

	# Delete all of the videos you just downloaded from the Arlo library.
	# Notice that you can pass the "library" object we got back from the GetLibrary() call.
	result = arlo.BatchDeleteRecordings(library)

	# If we made it here without an exception, then the videos were successfully deleted.
	print('Batch deletion of videos completed successfully.')

except Exception as e:
    print(e)
```

**For more code examples check out the [wiki](https://github.com/jeffreydwalter/arlo/wiki)**

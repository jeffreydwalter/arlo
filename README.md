![](logo.png)	
# arlo ![](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg)
> Python module for interacting with Netgear's Arlo camera system.
>
># ARLO IS IMPLEMENTING MANDITORY 2FA. THIS IS GOING TO MAKE THIS PACKAGE PERMENANTLY UNUSABLE!!! IT'S UP TO THE COMMUNITY TO MAKE THEIR VOICES HEARD! IF YOU USE THIS PACKAGE PLEASE GO LET THEM KNOW YOU DON'T WANT 2FA: https://community.arlo.com/t5/Arlo/Mandatory-Two-Step-Authentication-Verification-a-Bad-Idea/m-p/1760890#M4454
>
>### Now in Golang!
>If you love the Go programming language, check out [arlo-golang](https://github.com/jeffreydwalter/arlo-golang).
>My goal is to bring parity to the Python version asap. If you know what you're doing in Go, I would appreciate any feedback on the >general structure of the library, and contributions, etc.

---
### GETTING STARTED
Check out the [API DOCS](https://github.com/jeffreydwalter/arlo/tree/master/docs)

**IMPORTANT:** There is a regression in `sseclient 0.0.24` that breaks this package. Please ensure you have `seeclient 0.0.22` installed.

**IMPORTANT:** Please ensure you don't have ANY other `sseclient` packages installed in addition to `sseclient 0.0.22`! This may cause this package to fail in unexpected ways. A common one that is known to cause issues is the `sseclient-py 1.7` package. If you have a hard requirement to have more than one, please let me know and we can look into making that work.

**IMPORTANT:** my.arlo.com requires TLS 1.2 for their API. So, if you're getting ssl errors, it's most likely related to your version of openssl. You may need to upgrade your openssl library.
If you're running this library on OSX or macOS, they ship with `openssl v0.9.x` which does not support TLS 1.2. You should follow the instructions found [here](https://comeroutewithme.com/2016/03/13/python-osx-openssl-issue/) to upgrade your openssl library.

---
### Filing an Issue
Please read the [Issue Guidelines and Policies](https://github.com/jeffreydwalter/arlo/wiki/Issue-Guidelines-and-Policies) wiki page **BEFORE** you file an issue. Thanks.

---
## Install
```bash
# Install latest stable package
$ pip install arlo

--or--

# Install from master branch
$ pip install git+https://github.com/jeffreydwalter/arlo
```

---
This just a personal utility that I created out of necessity. It is by no means complete, although it does expose quite a bit of the Arlo interface in an easy to use Python pacakge. As such, this package does not come with unit tests (feel free to add them) or guarantees.
**All [contributions](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) are welcome and appreciated!**
--
**If you have a specific Arlo device that you want to improve support for, please consider sending me one! Since this project is solely maintained by yours truely and I don't have unlimited funds to support it, I can only really test and debug the code with the first gen Arlo cameras and basestation that I have. I also highly encourage and appreciate Pull Requests!**

**Please, feel free to [contribute](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) to this repo or buy Jeff a beer!** [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=R77B7UXMLA6ML&lc=US&item_name=Jeff%20Needs%20Beer&item_number=buyjeffabeer&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

---
### Generous Benefactors (Thank you!)
* [apsteinmetz](https://github.com/apsteinmetz) - 🍺
* [mhallikainen](https://github.com/mhallikainen) - 🍺🍺
* [tinsheep](https://github.com/tinsheep) - 🍺🍺
* [cubewot](https://github.com/cubewot) - 🍺🍺 
* [imopen](https://github.com/imopen) - 🍺 
* [notalifeform](https://github.com/notalifeform) - 🍺🍺
* [anonymous](https://github.com/jeffreydwalter/arlo) - 🍺🍺🍺🍺
* [kewashi](https://github.com/kewashi) - 🍺

---
### Awesomely Smart Contributors (Thank you!)
* [apsteinmetz](https://github.com/apsteinmetz) - Feb 12, 2020 - Added an example of timestamping Arlo snapshots to the wiki.
* [alvin-chang](https://github.com/alvin-chang) - Dec 15, 2019 - Updated some print statements to work with Python 3 in an example script.
* [pabloNZ](https://github.com/pabloNZ) - Jun 4, 2019 - Added the Arlo doorbell, Ultra camera and basestation schemas to the wiki.
* [m3ntalsp00n](https://github.com/m3ntalsp00n) - May 18, 2019 - Expanded ArloQ device support.
* [burken-](https://github.com/burken-) - Apr 17, 2019 - Fixed arming/disarming ArloQ devices.
* [m0urs](https://github.com/m0urs) - Apr 16, 2019 - Updated fqdn to new Arlo domain.
* [kimc78](https://github.com/kimc78) - Aug 16, 2018 - Added method to get CVR recording list.
* [jurgenweber](https://github.com/jurgenweber) - Apr 25, 2018 - Added Arlo Baby APIs!
* [pliablepixels](https://github.com/pliablepixels) - Apr 3, 2018 - Fixed up issues with the README.
* [manluk](https://github.com/manluk) - Mar 2, 2018 - Squashed a couple of bugs.
* [notalifeform](https://github.com/notalifeform) - Feb 10, 2018 - Fixed bug and formatting in example script.
* [erosen](https://github.com/erosen) - Jan 27, 2018 - Added the ArloQ camera schema to the wiki.
* [deanmcguire](https://github.com/deanmcguire) - Dec 7, 2017 - Unravelled the mysteries of RTSP streaming video.
* [andijakl](https://github.com/andijakl) - Jul 24, 2017 - Added Python 3 support and cleaned up examples.
* [cemeyer2](https://github.com/cemeyer2) - Nov 26, 2016 - Fixed setup issues.
* [LenShustek](https://github.com/LenShustek) - Sep 14, 2016, - Added Logout().

If You'd like to make a diffrence in the world and get your name on this most prestegious list, have a look at our [help wanted](https://github.com/jeffreydwalter/arlo/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) section!

After installing all of the required libraries, you can import and use this library like so:

```python
from arlo import Arlo

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
		#        f.write(video)
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

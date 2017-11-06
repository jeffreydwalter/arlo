# arlo ![](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg)
> Python module for interacting with Netgear's Arlo camera system.

This just a personal utility that I created out of necessity. It is by no means complete, although it does expose quite a bit of the Arlo interface in an easy to use Python pacakge. As such, this package does not come with unit tests (feel free to add them) or guarantees.
**All contributions are welcome and appreciated!**

**Please, feel free to contribute to this repo or, buy Jeff a beer!** [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=R77B7UXMLA6ML&lc=US&item_name=Jeff%20Needs%20Beer&item_number=buyjeffabeer&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

---
### Generous Benefactors
[cubewot](https://github.com/cubewot) - $10.00 (Thanks for the two beers!)
[imopen](https://github.com/imopen) - $5.00 (Thanks for the beer!) 

---

To get started, just do the following:

They can be installed like so:
```bash
# Clone the git repository.
$ git clone https://github.com/jeffreydwalter/arlo.git

# Run the make command from the arlo repository directory to download and install all the dependencies.
$ cd arlo
$ make
```
or:
```bash
# Clone the git repository.
$ git clone https://github.com/jeffreydwalter/arlo.git

# Install the required libraries using pip.
$ pip install monotonic 
$ pip install requests
$ pip install sseclient 
```
**A proper pip package is coming soon...**

**NOTE: arlo.netgear.com requires TLS 1.2 for their API. So, if you're getting ssl errors, it's most likely related to your version of openssl. You must upgrade your openssl library.
If you're running this library on OSX or macOS, they ship with openssl v0.9.x which does not support TLS 1.2. You should follow the instructions found here https://comeroutewithme.com/2016/03/13/python-osx-openssl-issue/ to upgrade your openssl library.**

After installing all of the required libraries, you can import and use this library like so:

```python
from datetime import timedelta, date
from Arlo import Arlo
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
		#	 with open('videos/'+videofilename, 'w') as f:
		#        f.write(stream)
		#        f.close()
		# Or:
		#
		# Get video as a chunked stream; this function returns a generator.
		stream = arlo.StreamRecording(recording['presignedContentUrl'])
		with open('videos/'+videofilename, 'w') as f:
			for chunk in stream:
				# Support both Python 2.7 and 3.
				if sys.version[0] == '2':
					f.write(chunk)
				else:
					f.buffer.write(chunk)
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

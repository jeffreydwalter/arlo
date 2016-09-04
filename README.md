# arlo
> Python module for interacting with Netgear's Arlo camera system.

This just a personal utility that I created out of necessity. It is by no means complete, although it does expose quite a bit of the Arlo interface in an easy to use Python pacakge.

As such, this package does not come with unit tests (feel free to add them) or guarantees.

*I'm not a Python developer by trade and I don't plan on doing much more work on this library outside of fixing any bugs I find or adding any APIs I discover I need.*

**Please, feel free to contribute to this repo.**

To get started, just do:

```
$ git clone https://github.com/jeffreydwalter/arlo.git
```

Once you have the repository cloned, you can import and use it, like so:

```
from Arlo.Arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

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

	##
	# The videos produced by Arlo are pretty small, even in their longest, best quality settings,
	# but you should probably prefer the chunked stream (see below). 
	###    
	#    # Download the whole video into memory as a single chunk.
	#    video = arlo.GetRecording(recording['presignedContentUrl'])
	#	 with open(recording['name']+'.mp4', 'w') as f:
	#        f.write(stream)
	#        f.close()
	# Or:
	#
	# Get video as a chunked stream; this function returns a generator.
	stream = arlo.StreamRecording(recording['presignedContentUrl']):
	with open(recording['name']+'.mp4', 'w') as f:
    	for chunk in stream:
        	f.write(chunk)
        f.close()

	print 'Downloaded video '+recording['name']+' from '+recording['createdDate']+'.'

# Delete all of the videos you just downloaded from the Arlo library.
# Notice that you can pass the "library" object we got back from the GetLibrary() call.
result = arlo.BatchDeleteRecordings(library)
if result['success'] == True:
	print 'Batch deletion of videos completed successfully.'
except Exception as e:
    print e
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

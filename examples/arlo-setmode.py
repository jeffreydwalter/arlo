from arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

	# Get the list of devices and filter on device type to only get the basestation.
	# This will return an array which includes all of the basestation's associated metadata.
	basestations = arlo.GetDevices('basestation')

	# Arm Arlo.
	arlo.Arm(basestations[0])
	# Or
	# Disarm Arlo.
	# arlo.Disarm(basestations[0])
        # Or
        # Change Mode to some custom mode you created.
        # arlo.CustomMode(basestations[0], "mode3") # 'mode3' is the id of a custom mode you created.
        # Or
        # Change Mode to Schedule.
        # arlo.CustomMode(basestations[0], mode=None, schedules=['schedules.1']) # 'schedules.1' is the id of my default schedule."

except Exception as e:
    print(e)

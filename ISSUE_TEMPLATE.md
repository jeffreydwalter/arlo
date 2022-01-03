Please answer these questions before submitting your issue. Thanks!


### What version of Python are you using (`python -V`)?


### What operating system and processor architecture are you using (`python -c 'import platform; print(platform.uname());'`)?


### Which Python packages do you have installed (run the `pip freeze` or `pip3 freeze` command and paste output)?
```
Paste your ouptut here
```

### Which version of ffmpeg are you using (`ffmpeg -version`)?
```
Paste your output here
```

### Which Arlo hardware are you having the issue with (camera types - [Arlo, Pro, Q, etc.], basestation model, etc.)?

### Run this script:
```
from arlo import Arlo

import json
import re

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'

def pp(data):
    print(json.dumps(data, indent=4, sort_keys=True))

try:
    arlo = Arlo(USERNAME, PASSWORD)
    
    devices = arlo.GetDevices()
    for i, device in enumerate(devices):
        for key in ['deviceId', 'parentId', 'uniqueId', 'userId', 'xCloudId']:
            if key in device:
                device[key] = re.sub(r'[0-9A-Za-z]', r'X', device.get(key))

        for key in ['deviceName', 'presignedFullFrameSnapshotUrl', 'presignedLastImageUrl', 'presignedSnapshotUrl']:
            device[key] = ""

        device['owner']['ownerId'] = re.sub(r'[0-9A-Za-z]', r'X', device['owner']['ownerId'])
        device['owner']['firstName'] = ""
        device['owner']['lastName'] = ""
        
        devices[i] = device

    pp(devices)
except Exception as e:
    print(e)
```

```
Paste your output here
```

### What did you do?

If possible, provide the steps you took to reproduce the issue. 
A complete runnable program is good. (don't include your user/password or any sensitive info)
```
Paste your ouptut here
```

### What did you expect to see?
```
Paste your ouptut here
```

### What did you see instead?
```
Paste your ouptut here
```

### Does this issue reproduce with the latest release?



##
# Copyright 2016 Jeffrey D. Walter
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

import json
import requests

class Arlo(object):
    def __init__(self, username, password):
	self.headers = {}
        self.Login(username, password)

    def get(self, url, caller):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        body = r.json()
        if body['success'] == True:
            if 'data' in body:
                return body['data']
        else:
            raise Exception(caller+' failed', body)

    def post(self, url, body, caller):
	r = requests.post(url, json=body, headers=self.headers)
	r.raise_for_status()
        body = r.json()
        if body['success'] == True:
            if 'data' in body:
                return body['data']
        else:
            raise Exception(caller+' failed', body)

    def put(self, url, body, caller):
	r = requests.put(url, json=body, headers=self.headers)
	r.raise_for_status()
        body = r.json()
        if body['success'] == True:
            if 'data' in body:
                return body['data']
        else:
            raise Exception(caller+' failed', body)

    #{
    #  "userId":"XXX-XXXXXXX",
    #  "email":"user@example.com",
    #  "token":"2_5HicFJMXXXXX-S_7IuK2EqOUHXXXXXXXXXXX1CXKWTThgU18Va_XXXXXX5S00hUafv3PV_if_Bl_rhiFsDHYwhxI3CxlVnR5f3q2XXXXXX-Wnt9F7D82uN1f4cXXXXX-FMUsWF_6tMBqwn6DpzOaIB7ciJrnr2QJyKewbQouGM6",
    #  "paymentId":"XXXXXXXX",
    #  "authenticated":1472961381,
    #  "accountStatus":"registered",
    #  "serialNumber":"XXXXXXXXXXXXX",
    #  "countryCode":"US",
    #  "tocUpdate":false,
    #  "policyUpdate":false,
    #  "validEmail":true
    #}
    def Login(self, username, password): 
        self.username = username
        self.password = password

        body = self.post('https://arlo.netgear.com/hmsweb/login', {'email': self.username, 'password': self.password}, 'Login')
	self.headers = {
	    'Authorization': body['token']
	}
	return body

    ##
    #
    # Set System Mode (Armed, Disarmed) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"modes","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"active":"mode0"}}
    # Set System Mode (Calendar) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"schedule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"active":true}}
    # Configure The Schedule (Calendar) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"schedule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"schedule":[{"modeId":"mode0","startTime":0},{"modeId":"mode2","startTime":28800000},{"modeId":"mode0","startTime":64800000},{"modeId":"mode0","startTime":86400000},{"modeId":"mode2","startTime":115200000},{"modeId":"mode0","startTime":151200000},{"modeId":"mode0","startTime":172800000},{"modeId":"mode2","startTime":201600000},{"modeId":"mode0","startTime":237600000},{"modeId":"mode0","startTime":259200000},{"modeId":"mode2","startTime":288000000},{"modeId":"mode0","startTime":324000000},{"modeId":"mode0","startTime":345600000},{"modeId":"mode2","startTime":374400000},{"modeId":"mode0","startTime":410400000},{"modeId":"mode0","startTime":432000000},{"modeId":"mode0","startTime":518400000}]}
    # Create Mode -
    #    {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"add","resource":"rules","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"name":"Record video on Camera 1 if Camera 1 detects motion","id":"ruleNew","triggers":[{"type":"pirMotionActive","deviceId":"XXXXXXXXXXXXX","sensitivity":80}],"actions":[{"deviceId":"XXXXXXXXXXXXX","type":"recordVideo","stopCondition":{"type":"timeout","timeout":15}},{"type":"sendEmailAlert","recipients":["__OWNER_EMAIL__"]},{"type":"pushNotification"}]}}
    #    {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"add","resource":"modes","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"name":"Test","rules":["rule3"]}}
    # Delete Mode - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"delete","resource":"modes/mode3","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true}
    # Camera Off - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"cameras/XXXXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"privacyActive":false}}
    # Night Vision On - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"cameras/XXXXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"zoom":{"topleftx":0,"toplefty":0,"bottomrightx":1280,"bottomrighty":720},"mirror":true,"flip":true,"nightVisionMode":1,"powerSaveMode":2}}
    # Motion Detection Test - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"cameras/XXXXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"motionSetupModeEnabled":true,"motionSetupModeSensitivity":80}}
    #
    # device_id = locations.data.uniqueIds
    #
    # System Properties: ("resource":"modes")
    #   active (string) - Mode Selection (mode2 = All Motion On, mode1 = Armed, mode0 = Disarmed, etc.)
    #
    # System Properties: ("resource":"schedule")
    #   active (bool) - Mode Selection (true = Calendar)
    #
    # Camera Properties: ("resource":"cameras/{id}")
    #   privacyActive (bool) - Camera On/Off
    #   zoom (topleftx (int), toplefty (int), bottomrightx (int), bottomrighty (int)) - Camera Zoom Level
    #   mirror (bool) - Mirror Image (left-to-right or right-to-left)
    #   flip (bool) - Flip Image Vertically
    #   nightVisionMode (int) - Night Mode Enabled/Disabled (1, 0)
    #   powerSaveMode (int) - PowerSaver Mode (3 = Best Video, 2 = Optimized, 1 = Best Battery Life) 
    #   motionSetupModeEnabled (bool) - Motion Detection Setup Enabled/Disabled 
    #   motionSetupModeSensitivity (int 0-100) - Motion Detection Sensitivity
    #
    ##
    def Notify(self, device_id, body):
	return self.post('https://arlo.netgear.com/hmsweb/users/devices/notify/'+device_id, body, 'Notify')

    def Reset(self):
        return self.get('https://arlo.netgear.com/hmsweb/users/library/reset', 'Reset')

    def GetServiceLevel(self):
        return self.get('https://arlo.netgear.com/hmsweb/users/serviceLevel', 'GetServiceLevel')

    def GetPaymentOffers(self):
        return self.get('https://arlo.netgear.com/hmsweb/users/payment/offers', 'GetPaymentOffers')

    def GetProfile(self):
	return self.get('https://arlo.netgear.com/hmsweb/users/profile', 'GetProfile')

    def GetFriends(self):
	return self.get('https://arlo.netgear.com/hmsweb/users/friends', 'GetFriends')

    #{
    #   "id":"XXX-XXXXXXX_20160823042047",
    #   "name":"Home",
    #   "ownerId":"XXX-XXXXXXX",
    #   "longitude":X.XXXXXXXXXXXXXXXX,
    #   "latitude":X.XXXXXXXXXXXXXXXX,
    #   "address":"123 Middle Of Nowhere Bumbfuck, EG, 12345",
    #   "homeMode":"schedule",
    #   "awayMode":"mode1",
    #   "geoEnabled":false,
    #   "geoRadius":150.0,
    #   "uniqueIds":[
    #      "XXX-XXXXXXX_XXXXXXXXXXXXX"
    #   ],
    #   "smartDevices":[
    #      "XXXXXXXXXX",
    #      "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    #   ],
    #   "pushNotifyDevices":[
    #      "XXXXXXXXXX"
    #   ]
    #}
    def GetLocations(self):
	return self.get('https://arlo.netgear.com/hmsweb/users/locations', 'GetLocations')

    def GetDevices(self):
        return self.get('https://arlo.netgear.com/hmsweb/users/devices', 'GetDevices')

    def GetLibraryMetaData(self, from_date, to_date):
        return self.post('https://arlo.netgear.com/hmsweb/users/library/metadata', {'dateFrom':from_date, 'dateTo':to_date}, 'GetRecordingMetaData')

    def UpdateProfile(self, first_name, last_name):
        return self.put('https://arlo.netgear.com/hmsweb/users/profile', {'firstName': first_name, 'lastName': last_name}, 'UpdateProfile')

    #{
    #  "firstName":"Some",
    #  "lastName":"Body",
    #  "devices":{
    #    "XXXXXXXXXXXXX":"Camera 1",
    #    "XXXXXXXXXXXXX":"Camera 2 ",
    #    "XXXXXXXXXXXXX":"Camera 3"
    #  },
    #  "lastModified":1463977440911,
    #  "adminUser":true,
    #  "email":"user@example.com",
    #  "id":"XXX-XXXXXXX"
    #}
    def UpdateFriends(self, body):
        return self.put('https://arlo.netgear.com/hmsweb/users/friends', body, 'UpdateFriends') 

    def UpdatePassword(self, password):
        r = self.post('https://arlo.netgear.com/hmsweb/users/changePassword', {'currentPassword':self.password,'newPassword':password}, 'ChangePassword')
        self.password = password
        return r

    def UpdateDeviceName(self, parent_id, device_id, name):
        return self.put('https://arlo.netgear.com/hmsweb/users/devices/renameDevice', {'deviceId':device_id, 'deviceName':name, 'parentId':parent_id}, 'UpdateDeviceName')

    def UpdateDisplayOrder(self, body):
        #{"devices":{"XXXXXXXXXXXXX":1,"XXXXXXXXXXXXX":2,"XXXXXXXXXXXXX":3}}
        return self.post('https://arlo.netgear.com/hmsweb/users/devices/displayOrder', body, 'UpdateDisplayOrder')

    #[
    # {
    #  "mediaDurationSecond": 30, 
    #  "contentType": "video/mp4", 
    #  "name": "XXXXXXXXXXXXX", 
    #  "presignedContentUrl": "https://arlos3-prod-z2.s3.amazonaws.com/XXXXXXX_XXXX_XXXX_XXXX_XXXXXXXXXXXXX/XXX-XXXXXXX/XXXXXXXXXXXXX/recordings/XXXXXXXXXXXXX.mp4?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1472968703&Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
    #  "lastModified": 1472881430181, 
    #  "localCreatedDate": XXXXXXXXXXXXX, 
    #  "presignedThumbnailUrl": "https://arlos3-prod-z2.s3.amazonaws.com/XXXXXXX_XXXX_XXXX_XXXX_XXXXXXXXXXXXX/XXX-XXXXXXX/XXXXXXXXXXXXX/recordings/XXXXXXXXXXXXX_thumb.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1472968703&Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
    #  "reason": "motionRecord", 
    #  "deviceId": "XXXXXXXXXXXXX", 
    #  "createdBy": "XXXXXXXXXXXXX", 
    #  "createdDate": "20160903", 
    #  "timeZone": "America/Chicago", 
    #  "ownerId": "XXX-XXXXXXX", 
    #  "utcCreatedDate": XXXXXXXXXXXXX, 
    #  "currentState": "new", 
    #  "mediaDuration": "00:00:30"
    # }
    #]
    def GetLibrary(self, from_date, to_date):
        return self.post('https://arlo.netgear.com/hmsweb/users/library', {'dateFrom':from_date, 'dateTo':to_date}, 'GetRecordings')

    def DeleteRecording(self, created_date, utc_created_date, device_id):
        return self.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':[{'createdDate':created_date,'utcCreatedDate':utc_created_date,'deviceId':device_id}]}, 'DeleteRecording')

    def BatchDeleteRecordings(self, recording_metadata):
        return self.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':recording_metadata}, 'BatchDeleteRecordings')

    def GetRecording(self, url, chunk_size=4096): 
        video = ''
        r = requests.get(url, stream=True)
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size): 
            if chunk: 
                video += chunk 
        return video

    def StreamRecording(self, url, chunk_size=4096):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size):
            yield chunk
    #{
    #  "to":"XXXXXXXXXXXXX",
    #  "from":"XXX-XXXXXXX_web",
    #  "resource":"cameras/XXXXXXXXXXXXX",
    #  "action":"set",
    #  "publishResponse":true,
    #  "transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX",
    #  "properties":{
    #      "activityState":"startPositionStream"
    #  }
    #}
    def StartStream(self, body):
	r = requests.post('https://arlo.netgear.com/hmsweb/users/devices/startStream', json=body, headers=self.headers)
	r.raise_for_status()
        body = r.json()
        if body['success'] == True:
            for stream in self.StreamRecording(body['data']['url']):
		yield stream
        else:
            raise Exception('StartStream returned False', body)

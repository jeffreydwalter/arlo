# `arlo` module

Copyright 2016 Jeffrey D. Walter

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS ISBASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

## Classes

` class Arlo `

    

### Class variables

`var TRANSID_PREFIX`

    

### Methods

` def __init__(self, username, password) `

    

Initialize self. See help(type(self)) for accurate signature.

` def AddFriend(self, firstname, lastname, email, devices={}, admin=False) `

    

This API will send an email to a user and if they accept, will give them
access to the devices you specify. NOTE: XXX-XXXXXXX_XXXXXXXXXXXX is the
uniqueId field in your device object.

{adminUser:false,firstName:John,lastName:Doe,email:john.doe@example.com,device
s:{XXX-XXXXXXX_XXXXXXXXXXXX:Camera1,XXX-XXXXXXX_XXXXXXXXXXXX:Camera2}}

` def AdjustBrightness(self, basestation, camera, brightness=0) `

    

NOTE: Brightness is between -2 and 2 in increments of 1 (-2, -1, 0, 1, 2).
Setting it to an invalid value has no effect.

Returns: { "action": "is", "from": "XXXXXXXXXXXXX", "properties": {
"brightness": -2 }, "resource": "cameras/XXXXXXXXXXXXX", "to":
"336-XXXXXXX_web", "transId": "web!XXXXXXXX.389518!1514956240683" }

` def AlertNotificationMethods(self, basestation, action='disabled',
email=False, push=False) `

    

**`action`** : `disabled` `OR` `recordSnapshot` `OR` `recordVideo`
     
` def Arm(self, device) `

    
` def BatchDeleteRecordings(self, recording_metadata) `

    

Delete a batch of video recordings from Arlo.

The GetLibrary() call response json can be passed directly to this method if
you'd like to delete the same list of videos you queried for. If you want to
delete some other batch of videos, then you need to send an array of objects
representing each video you want to delete.

[ { "createdDate":"20160904", "utcCreatedDate":1473010280395,
"deviceId":"XXXXXXXXXXXXX" }, { "createdDate":"20160904",
"utcCreatedDate":1473010280395, "deviceId":"XXXXXXXXXXXXX" } ]

` def Calendar(self, basestation, active=True) `

    

DEPRECATED: This API appears to still do stuff, but I don't see it called in
the web UI anymore when switching the mode to a schedule.

NOTE: The Arlo API seems to disable calendar mode when switching to other
modes, if it's enabled. You should probably do the same, although, the UI
reflects the switch from calendar mode to say armed mode without explicitly
setting calendar mode to inactive.

` def CustomMode(self, device, mode, schedules=[]) `

    

device can be any object that has parentId == deviceId. i.e., not a camera

` def DeleteMode(self, device, mode) `

    

device can be any object that has parentId == deviceId. i.e., not a camera

` def DeleteRecording(self, camera, created_date, utc_created_date) `

    

Delete a single video recording from Arlo. All of the date info and device id
you need to pass into this method are given in the results of the GetLibrary()
call.

` def Disarm(self, device) `

    
` def DownloadRecording(self, url, to) `

    

Writes a video to a given local file path.

**`url`** : `presignedContentUrl`
     
**`to`** : `path` `where` `the` `file` `should` `be` `written`
     
` def DownloadSnapshot(self, url, to, chunk_size=4096) `

    

Writes a snapshot to a given local file path.

**`url`** : `presignedContentUrl` or `presignedFullFrameSnapshotUrl`
     
**`to`** : `path` `where` `the` `file` `should` `be` `written`
     
` def Geofencing(self, location_id, active=True) `

    

Get location_id is the id field from the return of GetLocations() NOTE: The
Arlo API seems to disable geofencing mode when switching to other modes, if
it's enabled. You should probably do the same, although, the UI reflects the
switch from calendar mode to say armed mode without explicitly setting
calendar mode to inactive.

` def GetAudioPlayback(self, basestation) `

    
` def GetAutomationActivityZones(self, camera) `

    
` def GetAutomationDefinitions(self) `

    
` def GetBaseStationState(self, basestation) `

    
` def GetCalendar(self, basestation) `

    
` def GetCameraState(self, basestation) `

    
` def GetCameraTempReading(self, basestation) `

    
` def GetCvrPlaylist(self, camera, fromDate, toDate) `

    

This function downloads a Cvr Playlist file for the period fromDate to toDate.

` def GetDeviceCapabilities(self, device) `

    
` def GetDeviceSupport(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

This API looks like it's mainly used by the website, but I'm including it for
completeness sake. It returns something like the following: { "devices": [ {
"deviceType": "arloq", "urls": { "troubleshoot": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/pc_troubleshoot.html", "plugin":
"https://vzs3-prod-common.s3.amazonaws.com/static/html/en/pc_plugin.html",
"connection": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/pc_connection.html",
"connectionFailed": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/pc_connection_fail.html", "press_sync":
"https://vzs3-prod-common.s3.
amazonaws.com/static/html/en/pc_press_sync.html", "resetDevice": "https://vzs3
-prod-common.s3.amazonaws.com/static/html/en/reset_arloq.html", "qr_how_to":
"https://vzs3-prod-common.s3.amazonaws.com/static/html/en/pc_qr_how_to.html" }
}, { "deviceType": "basestation", "urls": { "troubleshoot": "https://vzs3
-prod-common.s3.amazonaws.com/static/html/en/bs_troubleshoot.html",
"connection": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/bs_connection.html", "sync":
"https://vzs3-prod-common.s3.amazonaws.com/static/html/en/bs_sync_camera.html"
} }, { "deviceType": "arloqs", "urls": { "ethernetSetup": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/ethernet_setup.html", "plugin":
"https:// vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/aqp_plugin.html",
"connectionWiFi": "https://vzs3-prod-common.s3.amazonaws.com/static/html/en/ar
loqs/connection_in_progress_wifi.html", "poeSetup": "https://vzs3-prod-
common.s3. amazonaws.com/static/html/en/arloqs/poe_setup.html", "connection":
"https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/connection_in_progress.html",
"connectionFailed": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/connection_fail.html",
"press_sync": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/press_sync.html",
"connectionType": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/connection_type.html",
"resetDevice": "https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/reset_device.html", "qr_how_to":
"https://vzs3-prod-
common.s3.amazonaws.com/static/html/en/arloqs/qr_how_to.html" } } ] }

` def GetDeviceSupportV3(self) `

    

This is the latest version of the device support api. It returns something
like the following: { "data": { "devices": { "camera": { "modelIds": [
"VMC3010", "VMC3030", "VMC4030", "VMC4030P", "VMC5040", "VZC3010", "VZC3030"
], "connectionTypes": { "WPS": true, "BLE": true }, "kbArticles": {
"insertBatteries": "https://kb.arlo.com/980150/Safety-Rules-for-Arlo-Wire-
Free-Camera-Batteries", "syncBasestation": "https://kb.arlo.com/987/How-do-I
-set-up-and-sync-my-Arlo-Wire-Free-cameras", "sync": "https://kb.arlo.com/987
/How-do-I-set-up-and-sync-my-Arlo-Wire-Free-camera", "firmwareUpdate":
"https://kb.arlo.com/4736/How-do-I-update-my-Arlo-firmware-manually" } },
"arloq": { "modelIds": [ "VMC3040", "VMC3040S" ], "kbArticles": { "power":
"https://kb.arlo.com/1001944/How-do-I-set-up-Arlo-Q-on-iOS", "qrCode":
"https://kb.arlo.com/1001944/How-do-I-set-up-Arlo-Q-on-iOS", "power_android":
"https://kb.arlo.com/1002006/How-do-I-set-up-Arlo-Q-on-Android",
"qrCode_android": "https://kb.arlo.com/1002006/How-do-I-set-up-Arlo-Q-on-
Android" } }, "basestation": { "modelIds": [ "VMB3010", "VMB4000",
"VMB3010r2", "VMB3500", "VZB3010", "VMB4500", "VMB5000" ], "smartHubs": [
"VMB5000" ], "kbArticles": { "pluginNetworkCable":
"https://kb.arlo.com/1179139/How-do-I-connect-my-Arlo-or-Arlo-Pro-base-
station-to-the-Internet", "power": "https://kb.arlo.com/1179139/How-do-I
-connect-my-Arlo-or-Arlo-Pro-base-station-to-the-Internet", "led":
"https://kb.arlo.com/1179139/How-do-I-connect-my-Arlo-or-Arlo-Pro-base-
station-to-the-Internet", "learnMore": "https://kb.arlo.com/000062124/How-do-I
-record-4K-videos-to-a-microSD-card" } }, "arlobaby": { "modelIds": [
"ABC1000" ], "kbArticles": { "power": "https://kb.arlo.com/1282682/How-do-I
-power-cycle-my-Arlo-Baby-camera", "qrCode": "https://kb.arlo.com/1282700/How-
do-I-set-up-my-Arlo-Baby-camera" } }, "lteCamera":{ "modelIds":[ "VML4030" ],
"kbArticles":{ "servicePlan":"https://kb.arlo.com/1286865/What-Arlo-Mobile-
service-plans-are-available", "simActivation":"https://kb.arlo.com/1286865
/What-Arlo-Mobile-service-plans-are-available",
"qrCode":"https://kb.arlo.com/1201822/How-do-I-set-up-my-Arlo-Go-camera" } },
"bridge": { "modelIds": [ "ABB1000" ], "kbArticles": { "power":
"https://kb.arlo.com/000062047", "sync": "https://kb.arlo.com/000062037",
"qrCode": "https://kb.arlo.com/000061886", "factoryReset":
"https://kb.arlo.com/000061837" } }, "lights": { "modelIds": [ "AL1101" ],
"kbArticles": { "sync": "https://kb.arlo.com/000062005", "insertBatteries":
"https://kb.arlo.com/000061952", "qrCode": "https://kb.arlo.com/000061886" }
}, "routerM1":{ "modelIds":[ "MR1100" ], "kbArticles":{
"lookupFailed":"https://kb.arlo.com/1179130/Arlo-can-t-discover-my-base-
station-during-installation-what-do-I-do" } }, "chime": { "modelIds": [
"AC1001" ], "kbArticles": { "ledNotBlinking":"https://kb.arlo.com/000061924",
"led":"https://kb.arlo.com/000061847",
"factoryReset":"https://kb.arlo.com/000061879",
"connectionFailed":"https://kb.arlo.com/000061880" } }, "doorbell": {
"modelIds": [ "AAD1001" ], "kbArticles": {
"led":"https://kb.arlo.com/000061847",
"factoryReset":"https://kb.arlo.com/000061842",
"pairCamera":"https://kb.arlo.com/000061897",
"existingChime":"https://kb.arlo.com/000061856",
"noWiring":"https://kb.arlo.com/000061859",
"connectionFailed":"https://kb.arlo.com/000061868",
"pairCameraFailed":"https://kb.arlo.com/000061893",
"testChimeFailed":"https://kb.arlo.com/000061944" }, "videos": { "chimeType":
"https://youtu.be/axytuF63VC0", "wireDoorbell":
"https://youtu.be/_5D2n3iPqW0", "switchSetting":
"https://youtu.be/BUmd4fik2RE" }, "arloVideos": { "chimeType": "https://vzs3
-prod-
common.s3.amazonaws.com/static/devicesupport/Arlo_Audio_Doorbell_Chime.mp4",
"wireDoorbell": "https://vzs3-prod-
common.s3.amazonaws.com/static/devicesupport/Arlo_Audio_Doorbell_Wired.mp4",
"switchSetting": "https://vzs3-prod-
common.s3.amazonaws.com/static/devicesupport/Arlo_Audio_Doorbell_Switch.mp4" }
} }, "arlosmart": { "kbArticles": { "e911": "https://www.arlo.com/en-
us/landing/arlosmart/", "callFriend": "https://www.arlo.com/en-
us/landing/arlosmart/", "4kAddOnPopup": "https://www.arlo.com/en-
us/landing/arlosmart/", "cloudRecording": "https://www.arlo.com/en-
us/landing/arlosmart/", "manageArloSmart": "https://kb.arlo.com/000062115",
"otherVideo": "https://kb.arlo.com/000062115", "packageDetection":
"https://kb.arlo.com/000062114", "whereIsBasicSubscriptionGone":
"https://kb.arlo.com/000062163" } } }, "success":true }

` def GetDeviceSupportv2(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

It returns something like the following: { "devices": [ { "deviceType":
"arloq", "modelId": [ "VMC3040" ], "urls": { "troubleshoot":
"arloq/troubleshoot.html", "plugin": "arloq/plugin.html", "qrHowTo":
"arloq/qrHowTo.html", "connection": "arloq/connection.html",
"connectionInProgress": "arloq/connectionInProgress.html", "connectionFailed":
"arloq/connectionFailed.html", "pressSync": "arloq/pressSync.html",
"resetDevice": "arloq/resetDevice.html" } }, { "deviceType": "basestation",
"modelId": [ "VMB3010", "VMB3010r2", "VMB3500", "VMB4000", "VMB4500",
"VZB3010" ], "urls": { "troubleshoot": "basestation/troubleshoot.html",
"plugin": "basestation/plugin.html", "sync3": "basestation/sync3.html",
"troubleshootBS": "basestation/troubleshootBS.html", "connection":
"basestation/connection.html", "connectionInProgress":
"basestation/connectionInProgress.html", "sync2": "basestation/sync2.html",
"connectionFailed": "basestation/connectionFailed.html", "sync1":
"basestation/sync1.html", "resetDevice": "basestation/resetDevice.html",
"syncComplete": "basestation/syncComplete.html" } }, { "deviceType":
"arlobaby", "modelId": [ "ABC1000" ], "urls": { "bleSetupError":
"arlobaby/bleSetupError.html", "troubleshoot": "arlobaby/troubleshoot.html",
"homekitCodeInstruction": "arlobaby/homekitCodeInstruction.html",
"connectionInProgress": "arlobaby/connectionInProgress.html",
"connectionFailed": "arlobaby/connectionFailed.html", "resetDevice":
"arlobaby/resetDevice.html", "plugin": "arlobaby/plugin.html", "qrHowTo":
"arlobaby/qrHowTo.html", "warning": "arlobaby/warning.html", "connection":
"arlobaby/connection.html", "pressSync": "arlobaby/pressSync.html",
"bleInactive": "arlobaby/bleInactive.html", "pluginIOS":
"arlobaby/pluginIOS.html", "homekitSetup": "arlobaby/homekitSetup.html" } }, {
"deviceType": "lteCamera", "modelId": [ "VML4030" ], "urls": { "troubleshoot":
"lteCamera/troubleshoot.html", "resetHowTo": "lteCamera/resetHowTo.html",
"plugin": "lteCamera/plugin.html", "qrHowTo": "lteCamera/qrHowTo.html",
"connectionInProgress": "lteCamera/connectionInProgress.html",
"connectionFailed": "lteCamera/connectionFailed.html", "resetDevice":
"lteCamera/resetHowTo.html", "resetComplete": "lteCamera/resetComplete.html",
"syncComplete": "lteCamera/syncComplete.html" } }, { "deviceType": "arloqs",
"modelId": [ "VMC3040S" ], "urls": { "ethernetSetup":
"arloqs/ethernetSetup.html", "troubleshoot": "arloqs/troubleshoot.html",
"plugin": "arloqs/plugin.html", "poeSetup": "arloqs/poeSetup.html",
"connectionInProgressWiFi": "arloqs/connectionInProgressWifi.html", "qrHowTo":
"arloqs/qrHowTo.html", "connectionInProgress":
"arloqs/connectionInProgress.html", "connectionFailed":
"arloqs/connectionFailed.html", "pressSync": "arloqs/pressSync.html",
"connectionType": "arloqs/connectionType.html", "resetDevice":
"arloqs/resetDevice.html" } }, { "deviceType": "bridge", "modelId": [
"ABB1000" ], "urls": { "troubleshoot": "bridge/troubleshoot.html",
"fwUpdateInProgress": "bridge/fwUpdateInProgress.html", "qrHowToUnplug":
"bridge/qrHowToUnplug.html", "fwUpdateDone": "bridge/fwUpdateDone.html",
"fwUpdateAvailable": "bridge/fwUpdateAvailable.html", "needHelp":
"https://www.arlo.com/en-us/support/#support_arlo_light", "wifiError":
"bridge/wifiError.html", "bleAndroid": "bridge/bleInactiveAND.html", "bleIOS":
"bridge/bleInactiveIOS.html", "connectionInProgress":
"bridge/connectionInProgress.html", "connectionFailed":
"bridge/connectionFailed.html", "manualPair": "bridge/manualPairing.html",
"resetDevice": "bridge/resetDevice.html", "lowPower":
"bridge/lowPowerZoneSetup.html", "fwUpdateFailed":
"bridge/fwUpdateFailed.html", "fwUpdateCheckFailed":
"bridge/fwUpdateCheckFailed.html", "plugin": "bridge/plugin.html", "qrHowTo":
"bridge/qrHowTo.html", "pressSync": "bridge/pressSync.html", "pluginNoLED":
"bridge/pluginNoLED.html", "fwUpdateCheck": "bridge/fwUpdateCheck.html" } }, {
"deviceType": "lights", "modelId": [ "AL1101" ], "urls": { "troubleshoot":
"lights/troubleshoot.html", "needHelp": "https://kb.netgear.com/000053159
/Light-discovery-failed.html", "bleInactiveAND": "lights/bleInactiveAND.html",
"connectionInProgress": "lights/connectionInProgress.html",
"connectionFailed": "lights/connectionFailed.html", "addBattery":
"lights/addBattery.html", "tutorial1": "lights/tutorial1.html", "plugin":
"lights/plugin.html", "tutorial2": "lights/tutorial2.html", "tutorial3":
"lights/tutorial3.html", "configurationInProgress":
"lights/configurationInProgress.html", "qrHowTo": "lights/qrHowTo.html",
"pressSync": "lights/pressSync.html", "bleInactiveIOS":
"lights/bleInactiveIOS.html", "syncComplete": "lights/syncComplete.html" } },
{ "deviceType": "routerM1", "modelId": [ "MR1100" ], "urls": { "troubleshoot":
"routerM1/troubleshoot.html", "help": "routerM1/help.html", "pairingFailed":
"routerM1/pairingFailed.html", "needHelp":
"https://acupdates.netgear.com/help/redirect.aspx?url=m1arlo-kbb", "plugin":
"routerM1/plugin.html", "pairing": "routerM1/pairing.html",
"connectionInProgress": "routerM1/connectionInProgress.html", "sync2":
"routerM1/sync2.html", "connectionFailed": "routerM1/connectionFailed.html",
"sync1": "routerM1/sync1.html", "sync": "routerM1/sync.html", "syncComplete":
"routerM1/syncComplete.html" } } ], "selectionUrls": { "addDevice":
"addDeviceBsRuAqAqpLteAbcMrBgLt.html", "selectBasestation": "selectBsMr.html",
"deviceSelection": "deviceBsAqAqpLteAbcMrLtSelection.html", "selectLights":
"selectBgLt.html" }, "baseUrl": "https://vzs3-prod-
common.s3.amazonaws.com/static/v2/html/en/" }

` def GetDevices(self, device_type=None) `

    

This method returns an array that contains the basestation, cameras, etc. and
their metadata. If you pass in a valid device type ('basestation', 'camera',
etc.), this method will return an array of just those devices that match that
type.

` def GetEmergencyLocations(self) `

    
` def GetFriends(self) `

    
` def GetLibrary(self, from_date, to_date) `

    

This call returns the following: presignedContentUrl is a link to the actual
video in Amazon AWS. presignedThumbnailUrl is a link to the thumbnail .jpg of
the actual video in Amazon AWS.

[ { "mediaDurationSecond": 30, "contentType": "video/mp4", "name":
"XXXXXXXXXXXXX", "presignedContentUrl":
"https://arlos3-prod-z2.s3.amazonaws.com/XXXXXXX_XXXX_XXXX_XXXX_XXXXXXXXXXXXX
/XXX-XXXXXXX/XXXXXXXXXXXXX/recordings/XXXXXXXXXXXXX.mp4?AWSAccessKeyId=XXXXXXX
XXXXXXXXXXXXX&Expires=1472968703&Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX", "lastModified": 1472881430181, "localCreatedDate": XXXXXXXXXXXXX,
"presignedThumbnailUrl":
"https://arlos3-prod-z2.s3.amazonaws.com/XXXXXXX_XXXX_XXXX_XXXX_XXXXXXXXXXXXX
/XXX-XXXXXXX/XXXXXXXXXXXXX/recordings/XXXXXXXXXXXXX_thumb.jpg?AWSAccessKeyId=X
XXXXXXXXXXXXXXXXXXX&Expires=1472968703&Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXX", "reason": "motionRecord", "deviceId": "XXXXXXXXXXXXX", "createdBy":
"XXXXXXXXXXXXX", "createdDate": "20160903", "timeZone": "America/Chicago",
"ownerId": "XXX-XXXXXXX", "utcCreatedDate": XXXXXXXXXXXXX, "currentState":
"new", "mediaDuration": "00:00:30" } ]

` def GetLibraryMetaData(self, from_date, to_date) `

    
` def GetLocations(self) `

    

This call returns the following: { "id":"XXX-XXXXXXX_20160823042047",
"name":"Home", "ownerId":"XXX-XXXXXXX", "longitude":X.XXXXXXXXXXXXXXXX,
"latitude":X.XXXXXXXXXXXXXXXX, "address":"123 Middle Of Nowhere Bumbfuck, EG,
12345", "homeMode":"schedule", "awayMode":"mode1", "geoEnabled":false,
"geoRadius":150.0, "uniqueIds":[ "XXX-XXXXXXX_XXXXXXXXXXXXX" ],
"smartDevices":[ "XXXXXXXXXX", "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" ],
"pushNotifyDevices":[ "XXXXXXXXXX" ] }

` def GetModes(self, basestation) `

    

DEPRECATED: This is the older API for getting the "mode". It still works, but
GetModesV2 is the way the Arlo software does it these days.

` def GetModesV2(self) `

    

This is the newer API for getting the "mode". This method also returns the
schedules. Set a non-schedule mode to be active: {"activeAutomations":[{"devic
eId":"XXXXXXXXXXXXX","timestamp":1532015622105,"activeModes":["mode1"],"active
Schedules":[]}]} Set a schedule to be active: {"activeAutomations":[{"deviceId
":"XXXXXXXXXXXXX","timestamp":1532015790139,"activeModes":[],"activeSchedules"
:["schedule.1"]}]}

` def GetOCProfile(self) `

    
` def GetPaymentBilling(self) `

    
` def GetPaymentOffers(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

` def GetPaymentOffersV2(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

` def GetPaymentOffersV3(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

` def GetPaymentOffersV4(self) `

    
` def GetProfile(self) `

    
` def GetRecording(self, url, chunk_size=4096) `

    

Returns the whole video from the presignedContentUrl.

` def GetRules(self, basestation) `

    
` def GetSensorConfig(self, basestation) `

    
` def GetServiceLevel(self) `

    
` def GetServiceLevelSettings(self) `

    
` def GetServiceLevelV2(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

` def GetServiceLevelV3(self) `

    

DEPRECATED: This API still works, but I don't see it being called in the web
UI anymore.

` def GetServiceLevelV4(self) `

    
` def GetSession(self) `

    

Returns something like the following: { "userId": "XXX-XXXXXXX", "email":
"jeffreydwalter@gmail.com", "token":
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "paymentId":
"XXXXXXXX", "accountStatus": "registered", "serialNumber": "XXXXXXXXXXXXXX",
"countryCode": "US", "tocUpdate": false, "policyUpdate": false, "validEmail":
true, "arlo": true, "dateCreated": 1463975008658 }

` def GetSmartAlerts(self, camera) `

    
` def GetSmartFeatures(self) `

    
` def GetUpdateFeatures(self) `

    
` def HandleEvents(self, basestation, callback, timeout=120) `

    

Use this method to subscribe to the event stream and provide a callback that
will be called for event event received. This function will allow you to
potentially write a callback that can handle all of the events received from
the event stream.

` def Login(self, username, password) `

    

This call returns the following: { "userId":"XXX-XXXXXXX",
"email":"user@example.com", "token":"2_5HicFJMXXXXX-S_7IuK2EqOUHXXXXXXXXXXX1CX
KWTThgU18Va_XXXXXX5S00hUafv3PV_if_Bl_rhiFsDHYwhxI3CxlVnR5f3q2XXXXXX-
Wnt9F7D82uN1f4cXXXXX-FMUsWF_6tMBqwn6DpzOaIB7ciJrnr2QJyKewbQouGM6",
"paymentId":"XXXXXXXX", "authenticated":1472961381,
"accountStatus":"registered", "serialNumber":"XXXXXXXXXXXXX",
"countryCode":"US", "tocUpdate":false, "policyUpdate":false, "validEmail":true
}

` def Logout(self) `

    
` def Notify(self, basestation, body) `

    

The following are examples of the json you would need to pass in the body of
the Notify() call to interact with Arlo:

######

######

**`NOTE`** : `While` `you` `can` `call` `Notify`() `directly`, `responses` `from` `these` `notify` `calls` `are` `sent` `to` `the` `EventStream` (`see` `Subscribe`()),
     

and so it's better to use the Get/Set methods that are implemented using the
NotifyAndGetResponse() method.

######

######

Set System Mode (Armed, Disarmed) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXX
XXX","action":"set","resource":"modes","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXX
XXXXX","publishResponse":true,"properties":{"active":"mode0"}} Set System Mode
(Calendar) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","re
source":"schedule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishRespo
nse":true,"properties":{"active":true}} Configure The Schedule (Calendar) -
{"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"sche
dule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"pr
operties":{"schedule":[{"modeId":"mode0","startTime":0},{"modeId":"mode2","sta
rtTime":28800000},{"modeId":"mode0","startTime":64800000},{"modeId":"mode0","s
tartTime":86400000},{"modeId":"mode2","startTime":115200000},{"modeId":"mode0"
,"startTime":151200000},{"modeId":"mode0","startTime":172800000},{"modeId":"mo
de2","startTime":201600000},{"modeId":"mode0","startTime":237600000},{"modeId"
:"mode0","startTime":259200000},{"modeId":"mode2","startTime":288000000},{"mod
eId":"mode0","startTime":324000000},{"modeId":"mode0","startTime":345600000},{
"modeId":"mode2","startTime":374400000},{"modeId":"mode0","startTime":41040000
0},{"modeId":"mode0","startTime":432000000},{"modeId":"mode0","startTime":5184
00000}]} Create Mode - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action"
:"add","resource":"rules","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publi
shResponse":true,"properties":{"name":"Record video on Camera 1 if Camera 1
detects motion","id":"ruleNew","triggers":[{"type":"pirMotionActive","deviceId
":"XXXXXXXXXXXXX","sensitivity":80}],"actions":[{"deviceId":"XXXXXXXXXXXXX","t
ype":"recordVideo","stopCondition":{"type":"timeout","timeout":15}},{"type":"s
endEmailAlert","recipients":["**OWNER_EMAIL**"]},{"type":"pushNotification"}]}
} {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"add","resource":"mo
des","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"pro
perties":{"name":"Test","rules":["rule3"]}} Delete Mode - {"from":"XXX-XXXXXXX
_web","to":"XXXXXXXXXXXXX","action":"delete","resource":"modes/mode3","transId
":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true} Camera Off -
{"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"came
ras/XXXXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishRespo
nse":true,"properties":{"privacyActive":false}} Night Vision On - {"from
":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"cameras/XX
XXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":t
rue,"properties":{"zoom":{"topleftx":0,"toplefty":0,"bottomrightx":1280,"botto
mrighty":720},"mirror":true,"flip":true,"nightVisionMode":1,"powerSaveMode":2}
} Motion Detection Test - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","acti
on":"set","resource":"cameras/XXXXXXXXXXXXX","transId":"web!XXXXXXXX.XXXXXXXXX
XXXXXXXXXXX","publishResponse":true,"properties":{"motionSetupModeEnabled":tru
e,"motionSetupModeSensitivity":80}}

device_id = locations.data.uniqueIds

System Properties: ("resource":"modes") active (string) - Mode Selection
(mode2 = All Motion On, mode1 = Armed, mode0 = Disarmed, etc.)

System Properties: ("resource":"schedule") active (bool) - Mode Selection
(true = Calendar)

Camera Properties: ("resource":"cameras/{id}") privacyActive (bool) - Camera
On/Off zoom (topleftx (int), toplefty (int), bottomrightx (int), bottomrighty
(int)) - Camera Zoom Level mirror (bool) - Mirror Image (left-to-right or
right-to-left) flip (bool) - Flip Image Vertically nightVisionMode (int) -
Night Mode Enabled/Disabled (1, 0) powerSaveMode (int) - PowerSaver Mode (3 =
Best Video, 2 = Optimized, 1 = Best Battery Life) motionSetupModeEnabled
(bool) - Motion Detection Setup Enabled/Disabled motionSetupModeSensitivity
(int 0-100) - Motion Detection Sensitivity

` def NotifyAndGetResponse(self, basestation, body, timeout=120) `

    
` def PauseTrack(self, basestation) `

    
` def Ping(self, basestation) `

    
` def PlayTrack(self, basestation,
track_id='2391d620-e491-4412-99f6-e9a40d6046ed', position=0) `

    

Defaulting to 'hugh little baby', which is a supplied track. I hope the ID is
the same for all.

` def PushToTalk(self, camera) `

    
` def RemoveFriend(self, email) `

    

Removes a person you've granted access to.

email: email of user you want to revoke access from.

` def ResendFriendInvite(self, friend) `

    

This API will resend an invitation email to a user that you've AddFriend'd.
You will need to get the friend object by calling GetFriend() because it
includes a token that must be passed to this API.

**`friend`** : {`"ownerId"`:`"XXX`-`XXXXXXX"`,`"token"`:`"really` `long` `string` `that` `you` `get` `from` `the` `GetFriends`() `API"`,`"firstName"`:`"John"`,`"lastName"`:`"Doe"`,`"devices"`:{`"XXX`-`XXXXXXX_XXXXXXXXXXXX"`:`"Camera1"`,`"XXX`-`XXXXXXX_XXXXXXXXXXXX"`:`"Camera2"`},`"lastModified"`:`1548470485419`,`"adminUser"`:`false`,`"email"`:`"john.doe`@`example.com"`}
     
` def Reset(self) `

    
` def RestartBasestation(self, basestation) `

    
` def SetAirQualityAlertOff(self, basestation) `

    
` def SetAirQualityAlertOn(self, basestation) `

    
` def SetAirQualityAlertThresholdMax(self, basestation, number=700) `

    
` def SetAirQualityAlertThresholdMin(self, basestation, number=400) `

    
` def SetAirQualityRecordingOff(self, basestation) `

    
` def SetAirQualityRecordingOn(self, basestation) `

    
` def SetAudioAlertsOff(self, basestation, sensitivity=3) `

    
` def SetAudioAlertsOn(self, basestation, sensitivity=3) `

    
` def SetAutomationActivityZones(self, camera, zone, coords, color) `

    

An activity zone is the area you draw in your video in the UI to tell Arlo
what part of the scene to "watch". This method takes 4 arguments. camera: the
camera you want to set an activity zone for. name: "Zone 1" - the name of your
activity zone. coords: [{"x":0.37946943483275664,"y":0.3790983606557377},{"x":
0.8685121107266436,"y":0.3790983606557377},{"x":0.8685121107266436,"y":1},{"x"
:0.37946943483275664,"y":1}] - these coordinates are the bonding box for the
activity zone. color: 45136 - the color for your bounding box.

` def SetHumidityAlertOff(self, basestation) `

    
` def SetHumidityAlertOn(self, basestation) `

    
` def SetHumidityAlertThresholdMax(self, basestation, number=800) `

    
` def SetHumidityAlertThresholdMin(self, basestation, number=400) `

    
` def SetHumidityRecordingOff(self, basestation) `

    
` def SetHumidityRecordingOn(self, basestation) `

    
` def SetLoopBackModeContinuous(self, basestation) `

    
` def SetLoopBackModeSingleTrack(self, basestation) `

    
` def SetMotionAlertsOff(self, basestation, sensitivity=5) `

    
` def SetMotionAlertsOn(self, basestation, sensitivity=5) `

    
` def SetNightLightBrightness(self, basestation, level=200) `

    
` def SetNightLightColor(self, basestation, red=255, green=255, blue=255) `

    
` def SetNightLightMode(self, basestation, mode='rainbow') `

    

mode: rainbow or rgb.

` def SetNightLightOff(self, basestation) `

    
` def SetNightLightOn(self, basestation) `

    
` def SetNightLightTimerOff(self, basestation, time=0, timediff=300) `

    
` def SetNightLightTimerOn(self, basestation, time=1556818752, timediff=0) `

    
` def SetOCProfile(self, firstName, lastName, country='United States',
language='en', spam_me=0) `

    
` def SetSchedule(self, basestation, schedule) `

    

The following json is what was sent to the API when I edited my schedule. It
contains all of the data necessary to configure a whole week. It's a little
convoluted, but you can just play around with the scheduler in Chrome and
watch the schema that gets sent.

{ "schedule": [ { "duration": 600, "startActions": { "disableModes": [ "mode0"
], "enableModes": [ "mode1" ] }, "days": [ "Mo", "Tu", "We", "Th", "Fr", "Sa",
"Su" ], "startTime": 0, "type": "weeklyAction", "endActions": {
"disableModes": [ "mode1" ], "enableModes": [ "mode0" ] } }, { "duration":
360, "startActions": { "disableModes": [ "mode0" ], "enableModes": [ "mode2" ]
}, "days": [ "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su" ], "startTime": 1080,
"type": "weeklyAction", "endActions": { "disableModes": [ "mode2" ],
"enableModes": [ "mode0" ] } }, { "duration": 480, "startActions": {
"disableModes": [ "mode0" ], "enableModes": [ "mode3" ] }, "days": [ "Tu" ],
"startTime": 600, "type": "weeklyAction", "endActions": { "disableModes": [
"mode3" ], "enableModes": [ "mode0" ] } } ], "name": "", "id": "schedule.1",
"enabled": true }

` def SetShuffleOff(self, basestation) `

    
` def SetShuffleOn(self, basestation) `

    
` def SetSleepTimerOff(self, basestation, time=0, timediff=300) `

    
` def SetSleepTimerOn(self, basestation, time=1556818752, timediff=0) `

    
` def SetTempAlertOff(self, basestation) `

    
` def SetTempAlertOn(self, basestation) `

    
` def SetTempAlertThresholdMax(self, basestation, number=240) `

    
` def SetTempAlertThresholdMin(self, basestation, number=200) `

    
` def SetTempRecordingOff(self, basestation) `

    
` def SetTempRecordingOn(self, basestation) `

    
` def SetTempUnit(self, uniqueId, unit='C') `

    
` def SetVolume(self, basestation, mute=False, volume=50) `

    
` def SirenOff(self, basestation) `

    
` def SirenOn(self, basestation) `

    
` def SkipTrack(self, basestation) `

    
` def StartRecording(self, basestation, camera) `

    

This function causes the camera to start recording. You can get the timezone
from GetDevices().

` def StartStream(self, basestation, camera) `

    

This function returns the url of the rtsp video stream. This stream needs to
be called within 30 seconds or else it becomes invalid. It can be streamed
with: ffmpeg -re -i 'rtsps://' -acodec copy -vcodec copy test.mp4 The request
to /users/devices/startStream returns: {
url:rtsp://:443/vzmodulelive?egressToken=b&userAgent=iOS&cameraId=}

` def StopRecording(self, camera) `

    

This function causes the camera to stop recording. You can get the timezone
from GetDevices().

` def StopStream(self, basestation, camera) `

    
` def StreamRecording(self, url, chunk_size=4096) `

    

Returns a generator that is the chunked video stream from the
presignedContentUrl.

**`url`** : `presignedContentUrl`
     
` def Subscribe(self, basestation) `

    

Arlo uses the EventStream interface in the browser to do pub/sub style
messaging. Unfortunately, this appears to be the only way Arlo communicates
these messages.

This function makes the initial GET request to /subscribe, which returns the
EventStream socket. Once we have that socket, the API requires a POST request
to /notify with the "subscriptionsresource. This call "registersthe device
(which should be the basestation) so that events will be sent to the
EventStream when subsequent calls to /notify are made.

Since this interface is asynchronous, and this is a quick and dirty hack to
get this working, I'm using a thread to listen to the EventStream. This thread
puts events into a queue. Some polling is required (see
NotifyAndGetResponse()) because the event messages aren't guaranteed to be
delivered in any specific order, but I wanted to maintain a synchronous style
API.

You generally shouldn't need to call Subscribe() directly, although I'm
leaving it "publicfor now.

` def SubscribeToMotionEvents(self, basestation, callback, timeout=120) `

    

Use this method to subscribe to motion events. You must provide a callback
function which will get called once per motion event.

The callback function should have the following signature: def callback(self,
event)

This is an example of handling a specific event, in reality, you'd probably
want to write a callback for HandleEvents() that has a big switch statement in
it to handle all the various events Arlo produces.

` def ToggleCamera(self, basestation, camera, active=True) `

    

active: True - Camera is off. active: False - Camera is on.

` def TriggerAndHandleEvent(self, basestation, trigger, callback, timeout=120)
`

    

Use this method to subscribe to the event stream and provide a callback that
will be called for event event received. This function will allow you to
potentially write a callback that can handle all of the events received from
the event stream. NOTE: Use this function if you need to run some code after
subscribing to the eventstream, but before your callback to handle the events
runs.

` def TriggerFullFrameSnapshot(self, basestation, camera) `

    

This function causes the camera to record a fullframe snapshot. The
presignedFullFrameSnapshotUrl url is returned. Use DownloadSnapshot() to
download the actual image file.

` def TriggerStreamSnapshot(self, basestation, camera) `

    

This function causes the camera to snapshot while recording. NOTE: You MUST
call StartStream() before calling this function. If you call StartStream(),
you have to start reading data from the stream, or streaming will be cancelled
and taking a snapshot may fail (since it requires the stream to be active).

NOTE: You should not use this function is you just want a snapshot and aren't
intending to stream. Use TriggerFullFrameSnapshot() instead.

NOTE: Use DownloadSnapshot() to download the actual image file.

` def Unsubscribe(self, basestation) `

    

This method stops the EventStream subscription and removes it from the
event_stream collection.

` def UpdateDeviceName(self, device, name) `

    
` def UpdateDisplayOrder(self, body) `

    

This is an example of the json you would pass in the body to
UpdateDisplayOrder() of your devices in the UI.

XXXXXXXXXXXXX is the device id of each camera. You can get this from
GetDevices(). { "devices":{ "XXXXXXXXXXXXX":1, "XXXXXXXXXXXXX":2,
"XXXXXXXXXXXXX":3 } }

` def UpdateFriend(self, body) `

    

This is an example of the json you would pass in the body: {
"firstName":"Some", "lastName":"Body", "devices":{ "XXXXXXXXXXXXX":"Camera 1",
"XXXXXXXXXXXXX":"Camera 2 ", "XXXXXXXXXXXXX":"Camera 3" },
"lastModified":1463977440911, "adminUser":true, "email":"user@example.com",
"id":"XXX-XXXXXXX" }

` def UpdatePassword(self, password) `

    
` def UpdateProfile(self, first_name, last_name) `

    
` def genTransId(self, trans_type='web') `

    
` def interrupt_handler(self, signum, frame) `

    
` def to_timestamp(self, dt) `

    

# Index

  * ### Classes

    * #### `Arlo`

      * `AddFriend`
      * `AdjustBrightness`
      * `AlertNotificationMethods`
      * `Arm`
      * `BatchDeleteRecordings`
      * `Calendar`
      * `CustomMode`
      * `DeleteMode`
      * `DeleteRecording`
      * `Disarm`
      * `DownloadRecording`
      * `DownloadSnapshot`
      * `Geofencing`
      * `GetAudioPlayback`
      * `GetAutomationActivityZones`
      * `GetAutomationDefinitions`
      * `GetBaseStationState`
      * `GetCalendar`
      * `GetCameraState`
      * `GetCameraTempReading`
      * `GetCvrPlaylist`
      * `GetDeviceCapabilities`
      * `GetDeviceSupport`
      * `GetDeviceSupportV3`
      * `GetDeviceSupportv2`
      * `GetDevices`
      * `GetEmergencyLocations`
      * `GetFriends`
      * `GetLibrary`
      * `GetLibraryMetaData`
      * `GetLocations`
      * `GetModes`
      * `GetModesV2`
      * `GetOCProfile`
      * `GetPaymentBilling`
      * `GetPaymentOffers`
      * `GetPaymentOffersV2`
      * `GetPaymentOffersV3`
      * `GetPaymentOffersV4`
      * `GetProfile`
      * `GetRecording`
      * `GetRules`
      * `GetSensorConfig`
      * `GetServiceLevel`
      * `GetServiceLevelSettings`
      * `GetServiceLevelV2`
      * `GetServiceLevelV3`
      * `GetServiceLevelV4`
      * `GetSession`
      * `GetSmartAlerts`
      * `GetSmartFeatures`
      * `GetUpdateFeatures`
      * `HandleEvents`
      * `Login`
      * `Logout`
      * `Notify`
      * `NotifyAndGetResponse`
      * `PauseTrack`
      * `Ping`
      * `PlayTrack`
      * `PushToTalk`
      * `RemoveFriend`
      * `ResendFriendInvite`
      * `Reset`
      * `RestartBasestation`
      * `SetAirQualityAlertOff`
      * `SetAirQualityAlertOn`
      * `SetAirQualityAlertThresholdMax`
      * `SetAirQualityAlertThresholdMin`
      * `SetAirQualityRecordingOff`
      * `SetAirQualityRecordingOn`
      * `SetAudioAlertsOff`
      * `SetAudioAlertsOn`
      * `SetAutomationActivityZones`
      * `SetHumidityAlertOff`
      * `SetHumidityAlertOn`
      * `SetHumidityAlertThresholdMax`
      * `SetHumidityAlertThresholdMin`
      * `SetHumidityRecordingOff`
      * `SetHumidityRecordingOn`
      * `SetLoopBackModeContinuous`
      * `SetLoopBackModeSingleTrack`
      * `SetMotionAlertsOff`
      * `SetMotionAlertsOn`
      * `SetNightLightBrightness`
      * `SetNightLightColor`
      * `SetNightLightMode`
      * `SetNightLightOff`
      * `SetNightLightOn`
      * `SetNightLightTimerOff`
      * `SetNightLightTimerOn`
      * `SetOCProfile`
      * `SetSchedule`
      * `SetShuffleOff`
      * `SetShuffleOn`
      * `SetSleepTimerOff`
      * `SetSleepTimerOn`
      * `SetTempAlertOff`
      * `SetTempAlertOn`
      * `SetTempAlertThresholdMax`
      * `SetTempAlertThresholdMin`
      * `SetTempRecordingOff`
      * `SetTempRecordingOn`
      * `SetTempUnit`
      * `SetVolume`
      * `SirenOff`
      * `SirenOn`
      * `SkipTrack`
      * `StartRecording`
      * `StartStream`
      * `StopRecording`
      * `StopStream`
      * `StreamRecording`
      * `Subscribe`
      * `SubscribeToMotionEvents`
      * `TRANSID_PREFIX`
      * `ToggleCamera`
      * `TriggerAndHandleEvent`
      * `TriggerFullFrameSnapshot`
      * `TriggerStreamSnapshot`
      * `Unsubscribe`
      * `UpdateDeviceName`
      * `UpdateDisplayOrder`
      * `UpdateFriend`
      * `UpdatePassword`
      * `UpdateProfile`
      * `__init__`
      * `genTransId`
      * `interrupt_handler`
      * `to_timestamp`

Generated by [pdoc 0.5.1](https://pdoc3.github.io/pdoc).


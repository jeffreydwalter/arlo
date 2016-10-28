##
# Copyright 2016 Jeffrey D. Walter
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from __future__ import division

import datetime
import math
import json
import random
import Queue
import requests
import sseclient
import threading
import time

class EventStream(object):
	def __init__(self, method, args):
		self.queue = Queue.Queue() 
		self.thread = threading.Thread(name="EventStream", target=method, args=(args))
		self.thread.setDaemon(True)
		self.thread.start()
		self.Disconnect()
		self.Unregister()
 
	def Connect(self):
		self.connected = True

	def Disconnect(self):
		self.connected = False

	def Register(self):
		self.registered = True

	def Unregister(self):
		self.registered = False

class Arlo(object):
	def __init__(self, username, password):
		self.cookies = {}
		self.headers = {}
		self.event_streams = {} 
		self.Login(username, password)

	def genTransId(self):

		def float2hex(f):
			MAXHEXADECIMALS = 15
			w = f // 1
			d = f % 1

			# Do the whole:
			if w == 0: result = '0'
			else: result = ''
			while w:
				w, r = divmod(w, 16)
				r = int(r)
				if r > 9: r = chr(r+55)
				else: r = str(r)
				result =  r + result

			# And now the part:
			if d == 0: return result

			result += '.'
			count = 0
			while d:
				d = d * 16
				w, d = divmod(d, 1)
				w = int(w)
				if w > 9: w = chr(w+55)
				else: w = str(w)
				result +=  w
				count += 1
				if count > MAXHEXADECIMALS: break

			return result

		now = datetime.datetime.today()
		return "web!" + float2hex(random.random() * math.pow(2, 32)).lower() + "!" + str(int((time.mktime(now.timetuple())*1e3 + now.microsecond/1e3))) 

	def get(self, url, caller, headers={}, cookies={}, stream=False):
		cookies.update(self.cookies)
		headers.update(self.headers)
		r = requests.get(url, headers=headers, cookies=cookies, stream=stream)
		if stream is True:
			return r
		r.raise_for_status()
		body = r.json()
		if body['success'] == True:
			if 'data' in body:
				return body['data']
		else:
			raise Exception(caller+' failed', body)

	def post(self, url, body, caller, headers={}, cookies={}):
		cookies.update(self.cookies)
		headers.update(self.headers)
		r = requests.post(url, json=body, cookies=cookies, headers=headers)
		r.raise_for_status()
		body = r.json()
		if body['success'] == True:
			if caller == 'Login':
				self.cookies = r.cookies

			if 'data' in body:
				return body['data']
		else:
			raise Exception(caller+' failed', body)

	def put(self, url, body, caller, headers={}, cookies={}):
		cookies.update(self.cookies)
		headers.update(self.headers)
		r = requests.put(url, json=body, cookies=cookies, headers=headers)
		r.raise_for_status()
		body = r.json()
		if body['success'] == True:
			if 'data' in body:
				return body['data']
		else:
			raise Exception(caller+' failed', body)

	##
	# This call returns the following:
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
	##
	def Login(self, username, password): 
		self.username = username
		self.password = password

		body = self.post('https://arlo.netgear.com/hmsweb/login', {'email': self.username, 'password': self.password}, 'Login')
		self.headers = {
			'DNT':'1',
			'Host': 'arlo.netgear.com',
			'Referer': 'https://arlo.netgear.com/',
			'Authorization': body['token']
		}
		
		self.user_id = body['userId'] 
		return body

	##
	# Arlo uses the EventStream interface in the browser to do pub/sub style messaging.
	# Unfortunately, this appears to be the only way Arlo communicates these messages.
	# 
	# This function makes the initial GET request to /subscribe, which returns the EventStream socket.
	# Once we have that socket, the API requires a POST request to /notify with the "subscriptions" resource.
	# This call "registers" the device (which should be the basestation) so that events will be sent to the EventStream
 	# when subsequent calls to /notify are made. 
	#
	# Since this interface is asyncronous, and this is a quick and dirty hack to get this working, I'm using a thread
	# to listen to the EventStream. This thread puts events into a Queue. Some polling is required (see NotifyAndGetResponse()) because
	# the event messages aren't guaranteed to be delivered in any specific order, but I wanted to maintain a synchronous style API.
	#
	# You generally shouldn't need to call Subscribe() directly, although I'm leaving it "public" for now. 
	##  
	def Subscribe(self, device_id, xcloud_id):
		def Register(self, device_id, xcloud_id):
			if device_id in self.event_streams and self.event_streams[device_id].connected: 
				self.Notify(device_id, xcloud_id, {"action":"set","resource":"subscriptions/"+self.user_id+"_web","publishResponse":"false","properties":{"devices":[device_id]}})
				event = self.event_streams[device_id].queue.get(block=True, timeout=1000)
				self.event_streams[device_id].Register()
				self.event_streams[device_id].queue.task_done()
				return event

		def QueueEvents(self, event_stream): 
			for event in event_stream:
				response = json.loads(event.data)
				if device_id in self.event_streams and self.event_streams[device_id].connected: 
					if 'action' in response and response['action'] == 'logout':
						self.event_streams[device_id].Disconnect()
					else:
						self.event_streams[device_id].queue.put(json.loads(event.data))
				elif 'status' in response and response['status'] == 'connected':
					self.event_streams[device_id].Connect()

		if device_id not in self.event_streams or not self.event_streams[device_id].connected: 
			event_stream = sseclient.SSEClient('https://arlo.netgear.com/hmsweb/client/subscribe?token='+self.headers['Authorization'], cookies=self.cookies)
			self.event_streams[device_id] = EventStream(QueueEvents, args=(self, event_stream,)) 
			while not self.event_streams[device_id].connected: 
				time.sleep(1)

		if not self.event_streams[device_id].registered: 
			Register(self, device_id, xcloud_id)

	##
	# This method stops the EventStream subscription and removes it from the event_stream collection. 
	##
	def Unsubscribe(self, device_id):
		if device_id in self.event_streams and self.event_streams[device_id].connected:
			print self.get('https://arlo.netgear.com/hmsweb/client/unsubscribe', 'Unsubscribe')
			self.event_stream[device_id].remove()

	##
	# The following are examples of the json you would need to pass in the body of the Notify() call to interact with Arlo:
	#
	###############################################################################################################################
	###############################################################################################################################
	# NOTE: While you can call Notify() directly, responses from these notify calls are sent to the EventStream (see Subscribe()),
	# and so it's better to use the Get/Set methods that are implemented using the NotifyAndGetResponse() method.
	###############################################################################################################################
	###############################################################################################################################
    #
	# Set System Mode (Armed, Disarmed) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"modes","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"active":"mode0"}}
	# Set System Mode (Calendar) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"schedule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"active":true}}
	# Configure The Schedule (Calendar) - {"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"set","resource":"schedule","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"schedule":[{"modeId":"mode0","startTime":0},{"modeId":"mode2","startTime":28800000},{"modeId":"mode0","startTime":64800000},{"modeId":"mode0","startTime":86400000},{"modeId":"mode2","startTime":115200000},{"modeId":"mode0","startTime":151200000},{"modeId":"mode0","startTime":172800000},{"modeId":"mode2","startTime":201600000},{"modeId":"mode0","startTime":237600000},{"modeId":"mode0","startTime":259200000},{"modeId":"mode2","startTime":288000000},{"modeId":"mode0","startTime":324000000},{"modeId":"mode0","startTime":345600000},{"modeId":"mode2","startTime":374400000},{"modeId":"mode0","startTime":410400000},{"modeId":"mode0","startTime":432000000},{"modeId":"mode0","startTime":518400000}]}
	# Create Mode -
	#	{"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"add","resource":"rules","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"name":"Record video on Camera 1 if Camera 1 detects motion","id":"ruleNew","triggers":[{"type":"pirMotionActive","deviceId":"XXXXXXXXXXXXX","sensitivity":80}],"actions":[{"deviceId":"XXXXXXXXXXXXX","type":"recordVideo","stopCondition":{"type":"timeout","timeout":15}},{"type":"sendEmailAlert","recipients":["__OWNER_EMAIL__"]},{"type":"pushNotification"}]}}
	#	{"from":"XXX-XXXXXXX_web","to":"XXXXXXXXXXXXX","action":"add","resource":"modes","transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX","publishResponse":true,"properties":{"name":"Test","rules":["rule3"]}}
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
	##
	def Notify(self, device_id, xcloud_id, body):
		body['transId'] = self.genTransId()
		body['from'] = self.user_id+'_web'
		body['to'] = device_id

		self.post('https://arlo.netgear.com/hmsweb/users/devices/notify/'+device_id, body, 'Notify', headers={"xCloudId":xcloud_id})
		return body['transId']

	def NotifyAndGetResponse(self, device_id, xcloud_id, body):
		self.Subscribe(device_id, xcloud_id)
		if device_id in self.event_streams and self.event_streams[device_id].connected and self.event_streams[device_id].registered: 
			transId = self.Notify(device_id, xcloud_id, body)
			event = self.event_streams[device_id].queue.get(block=True, timeout=1000)
			while event['transId'] != transId:
				print "ReQueuing transId: "+event['transId']
				self.event_streams[device_id].queue.put(event)
				event = self.event_streams[device_id].queue.get(block=True, timeout=1000)
				
			self.event_streams[device_id].queue.task_done()
			return event

	def GetBaseStation(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"get","resource":"basestation","publishResponse":"false"})

	def GetCameras(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"get","resource":"cameras","publishResponse":"false"})

	def GetRules(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"get","resource":"rules","publishResponse":"false"})

	def GetModes(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"get","resource":"modes","publishResponse":"false"})

	def Arm(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"set","resource":"modes","publishResponse":"true","properties":{"active":"mode1"}})

	def Disarm(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"set","resource":"modes","publishResponse":"true","properties":{"active":"mode0"}})

	def Calendar(self, device_id, xcloud_id):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"set","resource":"schedule","publishResponse":"true","properties":{"active":"true"}})

	def CustomMode(self, device_id, xcloud_id, mode):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"set","resource":"modes","publishResponse":"true","properties":{"active":mode}})

	def DeleteMode(self, device_id, xcloud_id, mode):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"delete","resource":"modes/"+mode,"publishResponse":"true"})

	def ToggleCamera(self, device_id, xcloud_id, active=True):
		return self.NotifyAndGetResponse(device_id, xcloud_id, {"action":"set","resource":"cameras/"+device_id,"publishResponse":"true","properties":{"privacyActive":active}})

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

	##
	# This call returns the following:
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
	#	  "XXX-XXXXXXX_XXXXXXXXXXXXX"
	#   ],
	#   "smartDevices":[
	#	  "XXXXXXXXXX",
	#	  "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
	#   ],
	#   "pushNotifyDevices":[
	#	  "XXXXXXXXXX"
	#   ]
	#}
	##
	def GetLocations(self):
		return self.get('https://arlo.netgear.com/hmsweb/users/locations', 'GetLocations')

	##
	# This method returns an array that contains the basestation, cameras, etc. and their metadata.
	#
	## 
	def GetDevices(self, device_type=None): 
		return self.get('https://arlo.netgear.com/hmsweb/users/devices', 'GetDevices')

	def GetLibraryMetaData(self, from_date, to_date):
		return self.post('https://arlo.netgear.com/hmsweb/users/library/metadata', {'dateFrom':from_date, 'dateTo':to_date}, 'GetRecordingMetaData')

	def UpdateProfile(self, first_name, last_name):
		return self.put('https://arlo.netgear.com/hmsweb/users/profile', {'firstName': first_name, 'lastName': last_name}, 'UpdateProfile')

	def UpdatePassword(self, password):
		r = self.post('https://arlo.netgear.com/hmsweb/users/changePassword', {'currentPassword':self.password,'newPassword':password}, 'ChangePassword')
		self.password = password
		return r

	##
	# This is an example of the json you would pass in the body to UpdateFriends():
	#{
	#  "firstName":"Some",
	#  "lastName":"Body",
	#  "devices":{
	#	"XXXXXXXXXXXXX":"Camera 1",
	#	"XXXXXXXXXXXXX":"Camera 2 ",
	#	"XXXXXXXXXXXXX":"Camera 3"
	#  },
	#  "lastModified":1463977440911,
	#  "adminUser":true,
	#  "email":"user@example.com",
	#  "id":"XXX-XXXXXXX"
	#}
	##
	def UpdateFriends(self, body):
		return self.put('https://arlo.netgear.com/hmsweb/users/friends', body, 'UpdateFriends') 

	def UpdateDeviceName(self, parent_id, device_id, name):
		return self.put('https://arlo.netgear.com/hmsweb/users/devices/renameDevice', {'deviceId':device_id, 'deviceName':name, 'parentId':parent_id}, 'UpdateDeviceName')

	##
	# This is an example of the json you would pass in the body to UpdateDisplayOrder() of your devices in the UI. 
	#
	# XXXXXXXXXXXXX is the device id of each camera. You can get this from GetDevices(). 
	#{
	#  "devices":{
	#	"XXXXXXXXXXXXX":1,
	#	"XXXXXXXXXXXXX":2,
	#	"XXXXXXXXXXXXX":3
	#  }
	#}
	##
	def UpdateDisplayOrder(self, body):
		return self.post('https://arlo.netgear.com/hmsweb/users/devices/displayOrder', body, 'UpdateDisplayOrder')

	##
	# This call returns the following:
	# presignedContentUrl is a link to the actual video in Amazon AWS.
	# presignedThumbnailUrl is a link to the thumbnail .jpg of the actual video in Amazon AWS.
	#
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
	##
	def GetLibrary(self, from_date, to_date):
		return self.post('https://arlo.netgear.com/hmsweb/users/library', {'dateFrom':from_date, 'dateTo':to_date}, 'GetRecordings')

	##
	# Delete a single video recording from Arlo.
	#
	# All of the date info and device id you need to pass into this method are given in the results of the GetLibrary() call.
	#
	##
	def DeleteRecording(self, created_date, utc_created_date, device_id):
		return self.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':[{'createdDate':created_date,'utcCreatedDate':utc_created_date,'deviceId':device_id}]}, 'DeleteRecording')

	##
	# Delete a batch of video recordings from Arlo.
	#
	# The GetLibrary() call response json can be passed directly to this method if you'd like to delete the same list of videos you queried for.
	# If you want to delete some other batch of videos, then you need to send an array of objects representing each video you want to delete.
	#
	#[  
	#  {  
	#	"createdDate":"20160904",
	#	"utcCreatedDate":1473010280395,
	#	"deviceId":"XXXXXXXXXXXXX"
	#  },
	#  {  
	#	"createdDate":"20160904",
	#	"utcCreatedDate":1473010280395,
	#	"deviceId":"XXXXXXXXXXXXX"
	#  }
	#]
	##
	def BatchDeleteRecordings(self, recording_metadata):
		return self.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':recording_metadata}, 'BatchDeleteRecordings')

	##
	# Returns the whole video from the presignedContentUrl. 
	#
	# Obviously, this function is generic and could be used to download anything. :)
	##
	def GetRecording(self, url, chunk_size=4096): 
		video = ''
		r = requests.get(url, stream=True)
		r.raise_for_status()

		for chunk in r.iter_content(chunk_size): 
			if chunk: video += chunk 
		return video

	##
	# Returns a generator that is the chunked video stream from the presignedContentUrl. 
	#
	# Obviously, this function is generic and could be used to download anything. :)
	##
	def StreamRecording(self, url, chunk_size=4096):
		r = requests.get(url, stream=True)
		r.raise_for_status()
		for chunk in r.iter_content(chunk_size):
			yield chunk
	##
	# This function returns a generator that is a chunked live video stream.
	#
	# To initiate a stream pass the following:
	#{
	#  "to":"XXXXXXXXXXXXX",
	#  "from":"XXX-XXXXXXX_web",
	#  "resource":"cameras/XXXXXXXXXXXXX",
	#  "action":"set",
	#  "publishResponse":true,
	#  "transId":"web!XXXXXXXX.XXXXXXXXXXXXXXXXXXXX",
	#  "properties":{
	#	  "activityState":"startPositionStream"
	#  }
	#}
	# The request to /users/devices/startStream returns:
	#{
	#  "data":{
	#	"url":"rtmps://vzwow09-z2-prod.vz.netgear.com:80/vzmodulelive?egressToken=b1b4b675_ac03_4182_9844_043e02a44f71&userAgent=web&cameraId=48B4597VD8FF5_1473010750131"
	#  },
	#  "success":true
	#}
	# which is the url of the video stream, which this function then uses to call StreamRecording().
	##
	def StartStream(self, body):
		body = self.post('https://arlo.netgear.com/hmsweb/users/devices/startStream', body, 'StartStream')
		for chunk in self.StreamRecording(body['url']):
			yield chunk 

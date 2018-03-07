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

# 14 Sep 2016, Len Shustek: Added Logout()
# 17 Jul 2017, Andreas Jakl: Port to Python 3 (https://www.andreasjakl.com/using-netgear-arlo-security-cameras-for-periodic-recording/)

import datetime
#import logging
import json
import math
import monotonic
import os
import random
import requests
import signal
import sseclient
import threading
import time
import sys
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue

#logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class EventStream(object):
    def __init__(self, event_handler, heartbeat_handler, args):
        self.connected = False
        self.registered = False
        self.queue = queue.Queue()
        self.heartbeat_stop_event = threading.Event()
        self.event_stream_stop_event = threading.Event()
        self.arlo = args[0]
        self.heartbeat_handler = heartbeat_handler

        try:
            event_stream = sseclient.SSEClient('https://arlo.netgear.com/hmsweb/client/subscribe?token='+self.arlo.request.session.headers.get('Authorization'), session=self.arlo.request.session)
            self.event_stream_thread = threading.Thread(name="EventStream", target=event_handler, args=(self.arlo, event_stream, self.event_stream_stop_event, ))
            self.event_stream_thread.setDaemon(True)
        except:
            pass

    def __del__(self):
        self.Disconnect()

    def Get(self, block=True, timeout=None):
        if sys.version[0] == '2' and block:
            if timeout:
                timeout += monotonic.monotonic()
            # If timeout is None, then just pick some arbitrarily large # for the timeout value.
            else:
                timeout = 1000000 + monotonic.monotonic()

            while True:
                try:
                    # Allow check for Ctrl-C every second
                    item = self.queue.get(timeout=min(1, timeout - monotonic.monotonic()))
                    self.queue.task_done()
                    return item
                except queue.Empty:
                    if monotonic.monotonic() > timeout:
                        raise
                    else:
                        pass
        else:
            item = self.queue.get(block=block, timeout=timeout)
            self.queue.task_done()
            return item

    def Start(self):
        self.event_stream_thread.start()
        return self

    def Connect(self):
        self.connected = True

    def Disconnect(self):
        self.connected = False
        self.Unregister()

    def Register(self):
        self.heartbeat_thread = threading.Thread(name='HeartbeatThread', target=self.heartbeat_handler, args=(self.arlo, self.heartbeat_stop_event, ))
        self.heartbeat_thread.setDaemon(True)
        self.heartbeat_thread.start()
        self.registered = True

    def Unregister(self):
        self.registered = False

        if self.queue:
            self.queue.put(None)

        self.event_stream_stop_event.set()
        self.heartbeat_stop_event.set()

        if self.event_stream_thread != threading.current_thread():
            self.event_stream_thread.join()

        if self.heartbeat_thread != threading.current_thread():
            self.heartbeat_thread.join()

class Request(object):
    """HTTP helper class"""

    def __init__(self):
        self.session = requests.Session()

    def _request(self, url, method='GET', params={}, headers={}, stream=False):
        if method == 'GET':
            r = self.session.get(url, headers=headers, stream=stream)
            if stream is True:
                return r
        elif method == 'PUT':
            r = self.session.put(url, json=params, headers=headers)
        elif method == 'POST':
            r = self.session.post(url, json=params, headers=headers)

        r.raise_for_status()
        body = r.json()
        if body['success'] == True:
            if 'data' in body:
                return body['data']
        else:
            raise Exception('Request ({0} {1}) failed'.format(method, url), body)

    def get(self, url, headers={}, stream=False):
        return self._request(url, 'GET', {}, headers, stream)

    def put(self, url, params={}, headers={}):
        return self._request(url, 'PUT', params, headers)

    def post(self, url, params={}, headers={}):
        return self._request(url, 'POST', params, headers)

class Arlo(object):
    TRANSID_PREFIX = 'web'
    def __init__(self, username, password):

        # signals only work in main thread
        try:
            signal.signal(signal.SIGINT, self.interrupt_handler)
        except:
            pass

        self.event_streams = {}
        self.request = None

        self.Login(username, password)

    def interrupt_handler(self, signum, frame):
        print("Caught Ctrl-C, exiting.")
        os._exit(1)

    def genTransId(self, trans_type=TRANSID_PREFIX):
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
        return trans_type+"!" + float2hex(random.random() * math.pow(2, 32)).lower() + "!" + str(int((time.mktime(now.timetuple())*1e3 + now.microsecond/1e3)))

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

        self.request = Request()

        body = self.request.post('https://arlo.netgear.com/hmsweb/login/v2', {'email': self.username, 'password': self.password})

        headers = {
            'DNT':'1',
            'Host': 'arlo.netgear.com',
            'Referer': 'https://arlo.netgear.com/',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B202 NETGEAR/v1 (iOS Vuezone)',
            'Authorization': body['token']
        }
        self.request.session.headers.update(headers)

        self.user_id = body['userId']
        return body

    def Logout(self):
        event_streams = self.event_streams.copy()
        for basestation_id in event_streams.keys():
            self.Unsubscribe(basestation_id)
        return self.request.put('https://arlo.netgear.com/hmsweb/logout')

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
    # to listen to the EventStream. This thread puts events into a queue. Some polling is required (see NotifyAndGetResponse()) because
    # the event messages aren't guaranteed to be delivered in any specific order, but I wanted to maintain a synchronous style API.
    #
    # You generally shouldn't need to call Subscribe() directly, although I'm leaving it "public" for now.
    ##
    def Subscribe(self, basestation):
        basestation_id = basestation.get('deviceId')

        def Register(self):
            if basestation_id in self.event_streams and self.event_streams[basestation_id].connected:
                self.Notify(basestation, {"action":"set","resource":"subscriptions/"+self.user_id+"_web","publishResponse":False,"properties":{"devices":[basestation_id]}})
                event = self.event_streams[basestation_id].Get(block=True, timeout=120)
                if event is None or self.event_streams[basestation_id].event_stream_stop_event.is_set():
                    return None
                elif event:
                    self.event_streams[basestation_id].Register()
                return event

        def QueueEvents(self, event_stream, stop_event):
            for event in event_stream:
                if event is None or stop_event.is_set():
                    return None

                response = json.loads(event.data)
                if basestation_id in self.event_streams:
                    if self.event_streams[basestation_id].connected:
                        if response.get('action') == 'logout':
                            self.event_streams[basestation_id].Disconnect()
                            return None
                        else:
                            self.event_streams[basestation_id].queue.put(response)
                    elif response.get('status') == 'connected':
                        self.event_streams[basestation_id].Connect()

        def Heartbeat(self, stop_event):
            while not stop_event.wait(2.0):
                try:
                    self.Ping(basestation)
                except queue.Empty:
                    pass

        if basestation_id not in self.event_streams or not self.event_streams[basestation_id].connected:
            self.event_streams[basestation_id] = EventStream(QueueEvents, Heartbeat, args=(self, ))
            self.event_streams[basestation_id].Start()
            while not self.event_streams[basestation_id].connected and not self.event_streams[basestation_id].event_stream_stop_event.is_set():
                time.sleep(0.5)

        if not self.event_streams[basestation_id].registered:
            Register(self)

    ##
    # This method stops the EventStream subscription and removes it from the event_stream collection.
    ##
    def Unsubscribe(self, basestation):
        if isinstance(basestation, str):
            basestation_id = basestation
        else:
            basestation_id = basestation.get('deviceId')
        if basestation_id in self.event_streams:
            if self.event_streams[basestation_id].connected:
                self.request.get('https://arlo.netgear.com/hmsweb/client/unsubscribe')
                self.event_streams[basestation_id].Disconnect()

            del self.event_streams[basestation_id]

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
    ##
    def Notify(self, basestation, body):
        basestation_id = basestation.get('deviceId')

        body['transId'] = self.genTransId()
        body['from'] = self.user_id+'_web'
        body['to'] = basestation_id

        self.request.post('https://arlo.netgear.com/hmsweb/users/devices/notify/'+body['to'], body, headers={"xcloudId":basestation.get('xCloudId')})
        return body.get('transId')

    def NotifyAndGetResponse(self, basestation, body, timeout=120):
        basestation_id = basestation.get('deviceId')

        self.Subscribe(basestation)

        if basestation_id in self.event_streams and self.event_streams[basestation_id].connected and self.event_streams[basestation_id].registered:
            transId = self.Notify(basestation, body)
            event = self.event_streams[basestation_id].Get(block=True, timeout=timeout)
            if event is None or self.event_streams[basestation_id].event_stream_stop_event.is_set():
                return None

            while basestation_id in self.event_streams and self.event_streams[basestation_id].connected and self.event_streams[basestation_id].registered and event.get('transId') != transId:
                self.event_streams[basestation_id].queue.put(event)
                event = self.event_streams[basestation_id].Get(block=True, timeout=timeout)
                if event is None or self.event_streams[basestation_id].event_stream_stop_event.is_set():
                    return None

            return event

    def Ping(self, basestation):
        basestation_id = basestation.get('deviceId')
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"subscriptions/"+self.user_id+"_web","publishResponse":False,"properties":{"devices":[basestation_id]}})

    # Use this method to subscribe to motion events. You must provide a callback function which will get called once per motion event.
    #
    # The callback function should have the following signature:
    #   def callback(self, event)
    #
    # This is an example of handling a specific event, in reality, you'd probably want to write a callback for HandleEvents()
    # that has a big switch statement in it to handle all the various events Arlo produces.
    def SubscribeToMotionEvents(self, basestation, callback, timeout=120):
        def callbackwrapper(self, event):
            if event.get('properties', {}).get('motionDetected'):
                callback(self, event)

        self.HandleEvents(basestation, callbackwrapper, timeout)

    # Use this method to subscribe to the event stream and provide a callback that will be called for event event received.
    # This function will allow you to potentially write a callback that can handle all of the events received from the event stream.
    def HandleEvents(self, basestation, callback, timeout=120):
        if not callable(callback):
            raise Exception('The callback(self, event) should be a callable function!')

        basestation_id = basestation.get('deviceId')

        self.Subscribe(basestation)
        if basestation_id in self.event_streams and self.event_streams[basestation_id].connected and self.event_streams[basestation_id].registered:
            while basestation_id in self.event_streams and self.event_streams[basestation_id].connected:
                event = self.event_streams[basestation_id].Get(block=True, timeout=timeout)
                if event is None and not self.event_streams[basestation_id].event_stream_stop_event.is_set():
                    return
                elif event is None:
                    continue;

                # If this event has is of resource type "subscriptions", then it's a ping reply event.
                # For now, these types of events will be requeued, since they are generated in response to and expected as a reply by the Ping() method.
                # HACK: Take a quick nap here to give the Ping() method's thread a chance to get the queued event.
                if event.get('resource', '').startswith('subscriptions'):
                    self.event_streams[basestation_id].queue.put(event)
                    time.sleep(0.05)
                else:
                    response = callback(self, event)
                    # NOTE: Not ideal, but this allows you to look for a specific event and break if you want to return it.
                    if response is not None:
                        return response

    # Use this method to subscribe to the event stream and provide a callback that will be called for event event received.
    # This function will allow you to potentially write a callback that can handle all of the events received from the event stream.
    # NOTE: Use this function if you need to run some code after subscribing to the eventstream, but before your callback to handle the events runs. 
    def TriggerAndHandleEvent(self, basestation, trigger, callback, timeout=120):
        if not callable(trigger):
            raise Exception('The trigger(self, camera) should be a callable function!')
        if not callable(callback):
            raise Exception('The callback(self, event) should be a callable function!')

        self.Subscribe(basestation)
        trigger(self)

        # NOTE: Calling HandleEvents() calls Subscribe() again, which basically turns into a no-op. Hackie I know, but it cleans up the code a bit.
        return self.HandleEvents(basestation, callback, timeout)

    def GetBaseStationState(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"get","resource":"basestation","publishResponse":False})

    def GetCameraState(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"get","resource":"cameras","publishResponse":False})

    def GetRules(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"get","resource":"rules","publishResponse":False})

    def GetModes(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"get","resource":"modes","publishResponse":False})

    def GetCalendar(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"get","resource":"schedule","publishResponse":False})

    def SirenOn(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"siren","publishResponse":True,"properties":{"sirenState":"on","duration":300,"volume":8,"pattern":"alarm"}})

    def SirenOff(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"siren","publishResponse":True,"properties":{"sirenState":"off","duration":300,"volume":8,"pattern":"alarm"}})

    def Arm(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"modes","publishResponse":True,"properties":{"active":"mode1"}})

    def Disarm(self, basestation):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"modes","publishResponse":True,"properties":{"active":"mode0"}})

    # NOTE: Brightness is between -2 and 2 in increments of 1 (-2, -1, 0, 1, 2).
    # Setting it to an invalid value has no effect.
    # Returns:
    #{
    #   "action": "is",
    #   "from": "XXXXXXXXXXXXX",
    #   "properties": {
    #       "brightness": -2
    #   },
    #   "resource": "cameras/XXXXXXXXXXXXX",
    #   "to": "336-XXXXXXX_web",
    #   "transId": "web!XXXXXXXX.389518!1514956240683"
    #}
    #
    def AdjustBrightness(self, basestation, camera, brightness=0):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"cameras/"+camera.get('deviceId'),"publishResponse":True,"properties":{"brightness":brightness}})

    # NOTE: The Arlo API seems to disable calendar mode when switching to other modes, if it's enabled.
    # You should probably do the same, although, the UI reflects the switch from calendar mode to say armed mode without explicitly setting calendar mode to inactive.
    def Calendar(self, basestation, active=True):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"schedule","publishResponse":True,"properties":{"active":active}})

    def CustomMode(self, basestation, mode):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"modes","publishResponse":True,"properties":{"active":mode}})

    def DeleteMode(self, basestation, mode):
        return self.NotifyAndGetResponse(basestation, {"action":"delete","resource":"modes/"+mode,"publishResponse":True})

    # Privacy active = True - Camera is off.
    # Privacy active = False - Camera is on.
    def ToggleCamera(self, basestation, camera, active=True):
        return self.NotifyAndGetResponse(basestation, {"action":"set","resource":"cameras/"+camera.get('deviceId'),"publishResponse":True,"properties":{"privacyActive":active}})

    def Reset(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/library/reset')

    def GetServiceLevel(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/serviceLevel')

    def GetPaymentOffers(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/payment/offers')

    def GetProfile(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/profile')

    ##
    # {"userId":"XXX-XXXXXXX","email":"jeffreydwalter@gmail.com","token":"2_5BtvCDVr5K_KJyGKaq8H61hLybT7D69krsmaZeCG0tvs-yw5vm0Y1LKVVoVI9Id19Fk9vFcGFnMja0z_5eNNqP_BOXIX9rzekS2SgTjz7Ao6mPzGs86_yCBPqfaCZCkr0ogErwffuFIZsvh_XGodqkTehzkfQ4Xl8u1h9FhqDR2z","paymentId":"XXXXXXXX","accountStatus":"registered","serialNumber":"XXXXXXXXXXXXXX","countryCode":"US","tocUpdate":false,"policyUpdate":false,"validEmail":true,"arlo":true,"dateCreated":1463975008658}
    ##
    def GetSession(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/session')

    def GetFriends(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/friends')

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
    ##
    def GetLocations(self):
        return self.request.get('https://arlo.netgear.com/hmsweb/users/locations')

    # Get location_id is the id field from the return of GetLocations()
    # NOTE: The Arlo API seems to disable geofencing mode when switching to other modes, if it's enabled.
    # You should probably do the same, although, the UI reflects the switch from calendar mode to say armed mode without explicitly setting calendar mode to inactive.
    def Geofencing(self, location_id, active=True):
        return self.request.put('https://arlo.netgear.com/hmsweb/users/locations/'+location_id, {"geoEnabled":active})

    ##
    # This method returns an array that contains the basestation, cameras, etc. and their metadata.
    # If you pass in a valid device type ('basestation', 'camera', etc.), this method will return an array of just those devices that match that type.
    ##
    def GetDevices(self, device_type=None):
        devices = self.request.get('https://arlo.netgear.com/hmsweb/users/devices')
        if device_type:
            return [ device for device in devices if device['deviceType'] == device_type]

        return devices

    def GetLibraryMetaData(self, from_date, to_date):
        return self.request.post('https://arlo.netgear.com/hmsweb/users/library/metadata', {'dateFrom':from_date, 'dateTo':to_date})

    def UpdateProfile(self, first_name, last_name):
        return self.request.put('https://arlo.netgear.com/hmsweb/users/profile', {'firstName': first_name, 'lastName': last_name})

    def UpdatePassword(self, password):
        r = self.request.post('https://arlo.netgear.com/hmsweb/users/changePassword', {'currentPassword':self.password,'newPassword':password})
        self.password = password
        return r

    ##
    # This is an example of the json you would pass in the body to UpdateFriends():
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
    ##
    def UpdateFriends(self, body):
        return self.request.put('https://arlo.netgear.com/hmsweb/users/friends', body)

    def UpdateDeviceName(self, device, name):
        return self.request.put('https://arlo.netgear.com/hmsweb/users/devices/renameDevice', {'deviceId':device.get('deviceId'), 'deviceName':name, 'parentId':device.get('parentId')})

    ##
    # This is an example of the json you would pass in the body to UpdateDisplayOrder() of your devices in the UI.
    #
    # XXXXXXXXXXXXX is the device id of each camera. You can get this from GetDevices().
    #{
    #  "devices":{
    #    "XXXXXXXXXXXXX":1,
    #    "XXXXXXXXXXXXX":2,
    #    "XXXXXXXXXXXXX":3
    #  }
    #}
    ##
    def UpdateDisplayOrder(self, body):
        return self.request.post('https://arlo.netgear.com/hmsweb/users/devices/displayOrder', body)

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
        return self.request.post('https://arlo.netgear.com/hmsweb/users/library', {'dateFrom':from_date, 'dateTo':to_date})

    ##
    # Delete a single video recording from Arlo.
    #
    # All of the date info and device id you need to pass into this method are given in the results of the GetLibrary() call.
    #
    ##
    def DeleteRecording(self, camera, created_date, utc_created_date):
        return self.request.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':[{'createdDate':created_date,'utcCreatedDate':utc_created_date,'deviceId':camera.get('deviceId')}]})

    ##
    # Delete a batch of video recordings from Arlo.
    #
    # The GetLibrary() call response json can be passed directly to this method if you'd like to delete the same list of videos you queried for.
    # If you want to delete some other batch of videos, then you need to send an array of objects representing each video you want to delete.
    #
    #[
    #  {
    #    "createdDate":"20160904",
    #    "utcCreatedDate":1473010280395,
    #    "deviceId":"XXXXXXXXXXXXX"
    #  },
    #  {
    #    "createdDate":"20160904",
    #    "utcCreatedDate":1473010280395,
    #    "deviceId":"XXXXXXXXXXXXX"
    #  }
    #]
    ##
    def BatchDeleteRecordings(self, recording_metadata):
        if recording_metadata:
            return self.request.post('https://arlo.netgear.com/hmsweb/users/library/recycle', {'data':recording_metadata})


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
    # url: presignedContentUrl
    #
    # Obviously, this function is generic and could be used to download anything. :)
    ##
    def StreamRecording(self, url, chunk_size=4096):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size):
            yield chunk

    ##
    # Writes a video to a given local file path.
    #
    # url: presignedContentUrl
    #
    # to: path where the file should be written
    ##
    def DownloadRecording(self, url, to):
        stream = self.StreamRecording(url)
        with open(to, 'wb') as fd:
            for chunk in stream:
                fd.write(chunk)
        fd.close()

    ##
    # Writes a snapshot to a given local file path.
    #
    # url: presignedContentUrl or presignedFullFrameSnapshotUrl
    #
    # to: path where the file should be written
    ##
    def DownloadSnapshot(self, url, to, chunk_size=4096):
        r = Request().get(url, stream=True)
        with open(to, 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
        fd.close()

    ##
    # This function returns the url of the rtsp video stream
    # This stream needs to be called within 30 seconds or else it becomes invalid
    # It can be streamed via ffmpeg -re -i 'rtsps://<url>' -acodec copy -vcodec copy test.mp4
    # The request to /users/devices/startStream returns:
    #{ "url":"rtsp://<url>:443/vzmodulelive?egressToken=b<xx>&userAgent=iOS&cameraId=<camid>" }
    #
    ##
    def StartStream(self, basestation, camera):
        
        # nonlocal variable hack for Python 2.x.
        class nl:
            stream_url_dict = None 

        def trigger(self):
            nl.stream_url_dict = self.request.post('https://arlo.netgear.com/hmsweb/users/devices/startStream', {"to":camera.get('parentId'),"from":self.user_id+"_web","resource":"cameras/"+camera.get('deviceId'),"action":"set","publishResponse":True,"transId":self.genTransId(),"properties":{"activityState":"startUserStream","cameraId":camera.get('deviceId')}}, headers={"xcloudId":camera.get('xCloudId')})

        def callback(self, event):
            if event.get("from") == basestation.get("deviceId") and event.get("resource") == "cameras/"+camera.get("deviceId") and event.get("properties", {}).get("activityState") == "userStreamActive":
                return nl.stream_url_dict['url'].replace("rtsp://", "rtsps://")

            return None

        return self.TriggerAndHandleEvent(basestation, trigger, callback)

    ##
    # This function causes the camera to snapshot while recording.
    # NOTE: You MUST call StartStream() before calling this function.
    # If you call StartStream(), you have to start reading data from the stream, or streaming will be cancelled
    # and taking a snapshot may fail (since it requires the stream to be active).
    #
    # NOTE: You should not use this function is you just want a snapshot and aren't intending to stream.
    # Use TriggerFullFrameSnapshot() instead.
    #
    # NOTE: Use DownloadSnapshot() to download the actual image file.
    ##
    def TriggerStreamSnapshot(self, basestation, camera):

        def trigger(self):
            self.request.post('https://arlo.netgear.com/hmsweb/users/devices/takeSnapshot', {'xcloudId':camera.get('xCloudId'),'parentId':camera.get('parentId'),'deviceId':camera.get('deviceId'),'olsonTimeZone':camera.get('properties', {}).get('olsonTimeZone')}, headers={"xcloudId":camera.get('xCloudId')})

        def callback(self, event):
            if event.get("deviceId") == camera.get("deviceId") and event.get("resource") == "mediaUploadNotification":
                presigned_content_url = event.get("presignedContentUrl")
                if presigned_content_url is not None:
                    return presigned_content_url

            return None

        return self.TriggerAndHandleEvent(basestation, trigger, callback)

    ##
    # This function causes the camera to record a fullframe snapshot.
    #
    # The presignedFullFrameSnapshotUrl url is returned.
    #
    # Use DownloadSnapshot() to download the actual image file.
    ##
    def TriggerFullFrameSnapshot(self, basestation, camera):

        def trigger(self):
            self.request.post("https://arlo.netgear.com/hmsweb/users/devices/fullFrameSnapshot", {"to":camera.get("parentId"),"from":self.user_id+"_web","resource":"cameras/"+camera.get("deviceId"),"action":"set","publishResponse":True,"transId":self.genTransId(),"properties":{"activityState":"fullFrameSnapshot"}}, headers={"xcloudId":camera.get("xCloudId")})

        def callback(self, event):
            if event.get("from") == basestation.get("deviceId") and event.get("resource") == "cameras/"+camera.get("deviceId") and event.get("action") == "fullFrameSnapshotAvailable":
                return event.get("properties", {}).get("presignedFullFrameSnapshotUrl")
            return None

        return self.TriggerAndHandleEvent(basestation, trigger, callback)

    ##
    # This function causes the camera to start recording.
    #
    # You can get the timezone from GetDevices().
    ##
    def StartRecording(self, basestation, camera):
        stream_url = self.StartStream(basestation, camera)
        self.request.post('https://arlo.netgear.com/hmsweb/users/devices/startRecord', {'xcloudId':camera.get('xCloudId'),'parentId':camera.get('parentId'),'deviceId':camera.get('deviceId'),'olsonTimeZone':camera.get('properties', {}).get('olsonTimeZone')}, headers={"xcloudId":camera.get('xCloudId')})
        return stream_url

    ##
    # This function causes the camera to stop recording.
    #
    # You can get the timezone from GetDevices().
    ##
    def StopRecording(self, camera):
        return self.request.post('https://arlo.netgear.com/hmsweb/users/devices/stopRecord', {'xcloudId':camera.get('xCloudId'),'parentId':camera.get('parentId'),'deviceId':camera.get('deviceId'),'olsonTimeZone':camera.get('properties', {}).get('olsonTimeZone')}, headers={"xcloudId":camera.get('xCloudId')})

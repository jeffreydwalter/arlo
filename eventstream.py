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

import monotonic
import sseclient
import threading
import sys

if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue

# TODO: There's a lot more refactoring that could/should be done to abstract out the arlo-specific implementation details.

class EventStream(object):
    """This class provides a queue-based EventStream object."""
    def __init__(self, event_handler, heartbeat_handler, args):
        self.event_handler = event_handler
        self.connected = False
        self.registered = False
        self.queue = queue.Queue()
        self.heartbeat_stop_event = threading.Event()
        self.event_stream_stop_event = threading.Event()
        self.arlo = args[0]
        self.heartbeat_handler = heartbeat_handler
 
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
                        return None
                    else:
                        pass
        else:
            try:
                item = self.queue.get(block=block, timeout=timeout)
                self.queue.task_done()
                return item
            except queue.Empty as e:
                return None
            except Exception as e:
                return None

    def Start(self):
        try:
            event_stream = sseclient.SSEClient('https://myapi.arlo.com/hmsweb/client/subscribe?token='+self.arlo.request.session.headers.get('Authorization').decode(), session=self.arlo.request.session)
            self.event_stream_thread = threading.Thread(name="EventStream", target=self.event_handler, args=(self.arlo, event_stream, self.event_stream_stop_event, ))
            self.event_stream_thread.setDaemon(True)
            self.event_stream_thread.start()
        except Exception as e:
            raise Exception('Failed to start eventstream thread: {0}'.format(e))


        return self

    def Connect(self):
        self.connected = True

    def Disconnect(self):
        self.connected = False
        self.Unregister()

    def Register(self):
        try:
            self.heartbeat_thread = threading.Thread(name='HeartbeatThread', target=self.heartbeat_handler, args=(self.arlo, self.heartbeat_stop_event, ))
            self.heartbeat_thread.setDaemon(True)
            self.heartbeat_thread.start()
            self.registered = True
        except Exception as e:
            raise Exception('Failed to start to heartbeat thread: {0}'.format(e))

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

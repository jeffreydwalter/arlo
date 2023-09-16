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

import requests
from requests.exceptions import HTTPError
from curl_cffi import requests as curl_cffi_requests

#from requests_toolbelt.utils import dump
#def print_raw_http(response):
#    data = dump.dump_all(response, request_prefix=b'', response_prefix=b'')
#    print('\n' * 2 + data.decode('utf-8'))

class Request(object):
    """HTTP helper class"""

    def __init__(self, impersonate=False):
        # we create different sessions based on different technical needs:
        # - curl_cffi is used to impersonate a browser and bypass client fingerprinting
        # - requests is used to produce a feature-filled Session that can be compatible with sseclient
        self.impersonate = impersonate
        if impersonate:
            self.session = curl_cffi_requests.Session(impersonate="chrome110")
        else:
            self.session = requests.Session()

    def _request(self, url, method='GET', params={}, headers={}, stream=False, raw=False):

        ## uncomment for debug logging
        """
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        req_log = logging.getLogger('requests.packages.urllib3')
        req_log.setLevel(logging.DEBUG)
        req_log.propagate = True
        """

        if method == 'GET':
            #print('COOKIES: ', self.session.cookies.get_dict())
            if self.impersonate:
                # curl_cffi does no suppot the stream keyword
                r = self.session.get(url, params=params, headers=headers)
            else:
                r = self.session.get(url, params=params, headers=headers, stream=stream)
            r.raise_for_status()
            if stream is True:
                return r
        elif method == 'PUT':
            r = self.session.put(url, json=params, headers=headers)
            r.raise_for_status()
        elif method == 'POST':
            r = self.session.post(url, json=params, headers=headers)
            r.raise_for_status()
        elif method == 'OPTIONS':
            r = self.session.options(url, headers=headers)
            r.raise_for_status()
            return

        body = r.json()

        if raw:
            return body
        else:
            if ('success' in body and body['success'] == True) or ('meta' in body and body['meta']['code'] == 200):
                if 'data' in body:
                    return body['data']
            else:
                raise HTTPError('Request ({0} {1}) failed: {2}'.format(method, url, r.json()), response=r)

    def get(self, url, params={}, headers={}, stream=False, raw=False):
        return self._request(url, 'GET', params=params, headers=headers, stream=stream, raw=raw)

    def put(self, url, params={}, headers={}, raw=False):
        return self._request(url, 'PUT', params=params, headers=headers, raw=raw)

    def post(self, url, params={}, headers={}, raw=False):
        return self._request(url, 'POST', params=params, headers=headers, raw=raw)

    def options(self, url, headers={}, raw=False):
        return self._request(url, 'OPTIONS', headers=headers, raw=raw)

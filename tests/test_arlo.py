# -*- coding: utf-8 -*-
import sys
import os
import pytest
import json
import responses
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'
LOGIN_JSON = json.load(open('./tests/responses/expected_login_response.json'))

class TestArlo(unittest.TestCase):
    def setUp(self):
        """
        """
        """
        mocked_login_url = "https://my.arlo.com/hmsweb/login/v2"

        responses.add(
            method = responses.POST,
            url = mocked_login_url,
            json = LOGIN_JSON,
            status = 200
        )
        """
        mocked_auth_url = "https://ocapi-app.arlo.com/api/auth"
        responses.add(
            method = responses.OPTIONS,
            url = mocked_auth_url,
            json = LOGIN_JSON,
            status = 200
        )
        responses.add(
            method = responses.POST,
            url = mocked_auth_url,
            json = LOGIN_JSON,
            status = 200
        )   

    @responses.activate
    def test_login(self):
        """
        """
        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.Login(USERNAME, PASSWORD)
        
        assert response["token"] == LOGIN_JSON["data"]["token"]

    @responses.activate
    def test_get_profile(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/profile"
        mock_json = {}

        with open('./tests/responses/expected_get_profile_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetProfile()
        
        assert response["firstName"] == mock_json["data"]["firstName"]
        assert response["lastName"] == mock_json["data"]["lastName"]
        
    @responses.activate
    def test_get_account(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/account"
        mock_json = {}

        with open('./tests/responses/expected_get_account_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetAccount()
        
        assert response["email"] == mock_json["data"]["email"]

    @responses.activate
    def test_get_devices(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/devices"
        mock_json = {}

        with open('./tests/responses/expected_get_devices_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetDevices()
        
        assert response[0]["deviceName"] == mock_json["data"][0]["deviceName"]

    @responses.activate
    def test_get_locations(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/locations"
        mock_json = {}

        with open('./tests/responses/expected_get_locations_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetLocations()
        
        assert response[0]["latitude"] == mock_json["data"][0]["latitude"]

    @responses.activate
    def test_get_friends(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/friends"
        mock_json = {}

        with open('./tests/responses/expected_get_friends_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetFriends()
        
        assert response[0]["email"] == mock_json["data"][0]["email"]

    @responses.activate
    def test_get_service_level_v4(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/serviceLevel/v4"
        mock_json = {}

        with open('./tests/responses/expected_get_service_level_v4_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetServiceLevelV4()
        
        assert response["planDetails"]["planId"] == mock_json["data"]["planDetails"]["planId"]

    @responses.activate
    def test_get_payment_offers_v4(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/payment/offers/v4"
        mock_json = {}

        with open('./tests/responses/expected_get_payment_offers_v4_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetPaymentOffersV4()
        
        assert response[0]["planId"] == mock_json["data"][0]["planId"]

    @responses.activate
    def test_get_modes_v2(self):
        """
        """
        mocked_url = "https://my.arlo.com/hmsweb/users/devices/automation/active"
        mock_json = {}

        with open('./tests/responses/expected_get_modes_v2_response.json') as json_file:
            mock_json = json.load(json_file)

        responses.add(
            method = responses.GET,
            url = mocked_url,
            json = mock_json,
            status = 200
        )

        arlo = Arlo(USERNAME, PASSWORD)
        response = arlo.GetModesV2()
        
        assert response[0]["uniqueId"] == mock_json["data"][0]["uniqueId"]

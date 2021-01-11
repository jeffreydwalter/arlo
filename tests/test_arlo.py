# -*- coding: utf-8 -*-
import sys
import os
import pytest
import json
import responses
import unittest
from http import HTTPStatus

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arlo import Arlo

USERNAME = 'user@example.com'
PASSWORD = 'supersecretpassword'
LOGIN_JSON = json.load(open('tests/responses/expected_login_response.json'))

class TestArlo(unittest.TestCase):
    def setUp(self):
        """
        """
        mocked_login_url = "https://my.arlo.com/hmsweb/login/v2"

        responses.add(
            method = responses.POST,
            url = mocked_login_url,
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
    def test_get_account(self):
        """
        """

        mocked_url = "https://my.arlo.com/hmsweb/users/account"
        mock_json = {}

        with open('tests/responses/expected_get_account_response.json') as json_file:
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
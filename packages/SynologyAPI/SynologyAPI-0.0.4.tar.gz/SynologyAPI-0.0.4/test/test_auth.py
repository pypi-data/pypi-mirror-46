#!/usr/bin/python3
# 2019-05-07
# Daniel Nicolas Gisolfi

import json
import pytest
from SynologyAPI.auth import Auth

class TestAuth:
    auth = Auth(
        'danielgisolfi',
        'nagcu3-cixkyz-xobhEm',
        'https://share.ecrl.marist.edu:5001'
    )


    # In order to test if the API can be called, 
    # lets get all info about the API to test the connection
    def testApiRequest(self):
        params =  {
            'version': 1,
            'method': 'query',
            'query': 'ALL'
        }

        response = self.auth.apiRequest('get', 'SYNO.API.Info', 'query.cgi', params)
        assert response.status_code == 200
        

    # When logging into the API a SYNO.API feild must be chosen
    # we only need FileStation so test the login and then ensure 
    # a session ID is returned.
    def testSessionLogin(self):
        response = self.auth.login('FileStation')
        response_json = json.loads(response.content)

        success = response_json['success']
        assert success == True
        sid = response_json['data']['sid']
        assert self.auth.sid == sid

    # The apiList function gets all the valid API calls 
    # in a dictionary, test wether the data is being returned
    def testApiList(self):
        response = self.auth.apiList()
        assert response.status_code == 200
        assert json.loads(response.content)['data'] != {}
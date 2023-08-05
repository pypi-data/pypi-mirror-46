#!/usr/bin/python3
# 2019-05-03
# Daniel Nicolas Gisolfi

import json
import requests

class Auth:
    def __init__(self, user, password, address):
        self.__user = user
        self.__password = password
        self.__addr = address+'/webapi/'
        self.__session = requests.Session()
        self.__sid = None

    @property
    def sid(self):
        return self.__sid

    @sid.setter
    def sid(self, sid):
        self.__sid = sid

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session):
        self.__session = session
    
    def apiRequest(self, method, api_name, path, params, data=None, files=None):
        try:
            if method == 'get':
                url = f'{self.__addr}{path}?api={api_name}'
                response = self.session.get(url, params=params)
            elif method == 'post':
                url = f'{self.__addr}{path}?api={api_name}'
                if data is not None and files is not None:
                    print(url)
                    response = self.session.post(url, data=data, files=files)
                else:
                    response = self.session.post(url, params=params)

            return response
        except:
            raise Exception(f'Error connecting to Synology API')


    def login(self, application):
            params = {
                'version': '3', 
                'method': 'login', 
                'account': self.__user,
                'passwd': self.__password, 
                'session': application, 
                'format': 'cookie'
            }

            response = self.apiRequest('get', 'SYNO.API.Auth', 'auth.cgi' , params)

            if response.status_code is not 200:
                raise Exception(f'Error loging in as user: {self.__user}')

            response_json = json.loads(response.content)
            self.sid = response_json['data']['sid']

            return response

    def apiList(self):
        path = 'query.cgi'
        params = {
            'version': '1', 
            'method': 'query', 
            'query': 'all'
        }

        response = self.apiRequest('get','SYNO.API.Info', 'query.cgi', params=params)

        return response

    
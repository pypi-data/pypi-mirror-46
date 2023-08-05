#!/usr/bin/python3
# 2019-05-03
# Daniel Nicolas Gisolfi

import os
import json
from SynologyAPI.auth import Auth

class FileStation:
    def __init__(self, user, password, address):
        self.__user = user
        self.__password = password
        self.__address = address
        self.__application = 'FileStation'
        self.auth = Auth(
            self.__user, 
            self.__password,
            self.__address
        )
        self.auth.login(self.__application)
        
    # This may not work in the current version of the API...
    def listFiles(self, file_path):

        params = {
            'version': '2', 
            'method': 'list', 
            '_sid': self.auth.sid,
            'path': file_path,
            'format': 'cookie'
        }

        response = self.auth.apiRequest('get', 'SYNO.FileStation.List', 'entry.cgi' , params)

        return response

    def getFileInfo(self, file_path):
        if file_path is None:
            raise Exception(f'file path cannot be none')

        params = {
            'version': '2', 
            'method': 'getinfo', 
            '_sid': self.auth.sid,
            'path': file_path,
            'format': 'cookie'
        }

        response = self.auth.apiRequest('get', 'SYNO.FileStation.List', 'entry.cgi' , params)

        return response

    def uploadFile(self, source_path, target_path):
        filename = os.path.basename(source_path)
        api_name = 'SYNO.FileStation.Upload'
        api_path = 'entry.cgi'

        try:
            payload = open(source_path, 'rb')
        except:
            raise Exception(f'Source file at {source_path} cannot be openend')

        args = {
            'path': target_path,
            'create_parents': False,
            'overwrite': True,
        }

        files = {'file': (filename, payload, 'application/octet-stream')}
        url = f'{self.__address}/webapi/{api_path}?api={api_name}&version=3&method=upload&_sid={self.auth.sid}'

        response = self.auth.session.post(url, data=args, files=files)

        payload.close()
        return response
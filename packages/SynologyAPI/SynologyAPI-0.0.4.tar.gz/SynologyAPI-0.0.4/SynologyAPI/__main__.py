#!/usr/bin/python3
# 2019-05-03
# Daniel Nicolas Gisolfi

import click
import json
from SynologyAPI.filestation import FileStation

@click.command()
@click.argument('method')
@click.argument('user')
@click.argument('password')
@click.argument('synology_address')
@click.argument('source', type=click.Path())
@click.argument('target', type=click.Path())
def main(method, user, password, synology_address, source, target):
    fileManager = FileStation(user, password, synology_address)
    if method == 'upload':
        reponse = fileManager.uploadFile(source, target)
        try:
            response_json = json.loads(response.content)
            print(f'success = {response_json["success"]}')
        except:
            print('File Upload Failure')
    elif method == 'file_info':
        # try:
        response = fileManager.getFileInfo('/HoneypotLogs/HoneynetLogs/2019-02.tar.gz')
        response_json = json.loads(response.content)
        print(response_json)
            # print(f'success = {response_json["success"]}')
        # except:
        #     print('File Info request Failure')

if __name__ == "__main__":
    main()


# python3 ./src danielgisolfi nagcu3-cixkyz-xobhEm https://share.ecrl.marist.edu:5001 /Users/daniel/git/SynologyAPI/README.md /HoneypotLogs/HoneynetLogs


# python3 ./src file_info danielgisolfi nagcu3-cixkyz-xobhEm https://share.ecrl.marist.edu:5001 /Users/daniel/git/SynologyAPI/README.md /HoneypotLogs/HoneynetLogs

# danielgisolfi nagcu3-cixkyz-xobhEm https://share.ecrl.marist.edu:5001 $(pwd)/README.md /HoneypotLogs/HoneynetLogs

# danielgisolfi nagcu3-cixkyz-xobhEm https://share.ecrl.marist.edu:5001 $(pwd)/2019-02.tar.gz /HoneypotLogs/HoneynetLogs
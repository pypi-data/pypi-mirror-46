#!/usr/bin/python3
# 2019-05-03
# Daniel Nicolas Gisolfi

import click
from filestation import FileStation

@click.command()
@click.argument('user')
@click.argument('password')
@click.argument('synology_address')
@click.argument('source', type=click.Path())
@click.argument('target', type=click.Path())
def main(user, password, synology_address, source, target):
    fileManager = FileStation(user, password, synology_address)
    fileManager.uploadFile(source, target)

if __name__ == "__main__":
    main()


# python3 ./src danielgisolfi nagcu3-cixkyz-xobhEm https://share.ecrl.marist.edu:5001 /Users/daniel/git/SynologyAPI/README.md /HoneypotLogs/HoneynetLogs
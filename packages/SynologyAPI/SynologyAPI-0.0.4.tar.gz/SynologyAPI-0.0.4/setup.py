#!/usr/bin/python3
from setuptools import setup

setup(
    name='SynologyAPI',
    version='0.0.4',
    description='A simple wrapper for some of the functions that the Synology API supports.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Marist-SDN-SecureCloud/SynologyAPI',
    license='MIT',
    packages=['SynologyAPI'],
    install_requires=[
        'click>=7.0',
        'requests>=2.21.0'
    ],
    zip_safe=False,
    entry_points='''
    [console_scripts]
    synology=src.__main__:main
    '''
)
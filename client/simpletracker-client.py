#!/bin/usr/env python

import FolderInfo
import json
import sys
import requests

class STClientInstance(object):

    def __init__(self, server):
        self.server = server
        self.headers = {'Content-type': 'application/json'}

    def post(self, endpoint, data)
        try:
            response = requests.post(endpoint, headers = self.headers, data = data)

    def register(self, ip, ctl_port):
        endpoint = "/regi"
    def deregister(self, ip):
        endpoint = "/deregi"
    def update(self):
        endpoint = "/update"

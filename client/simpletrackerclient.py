#!/bin/usr/env python

import json
import requests
import traceback
import folderinfo


class STClientInstance(object):

    def __init__(self, server, folderpath, root_uri):
        self.server = server
        self.folderpath = folderpath
        self.root_uri = root_uri
        self.headers = {'Content-type': 'application/json'}

    def post(self, endpoint, data):
        try:
            response = requests.post(endpoint, headers=self.headers, data=data)
        except requests.exceptions.RequestException as e:
            print(traceback.print_exc())
        return response

    def delete(self, endpoint, data):
        try:
            response = requests.delete(endpoint, headers=self.headers, data=data)
        except requests.exceptions.RequestException as e:
            print(traceback.print_exc())
        return response


    def parse_response(self, response):
        result = json.loads(response)
        if result["status"] == "OK":
            print("success")
        else:
            print("fail")

    def register(self, ip, ctl_port):
        endpoint = "/register"
        data = {
            "ip": ip,
            "ctl_port": ctl_port
        }
        json_data = json.dumps(data)
        response = self.post(endpoint=self.server+endpoint,
                             data=json_data)
        self.parse_response(response.text)

    def deregister(self, ip):
        endpoint = "/deregister"
        data = {
            "ip": ip
        }
        json_data = json.dumps(data)
        print(json_data)
        response = self.delete(endpoint=self.server+endpoint,
                             data=json_data)
        self.parse_response(response.text)

    def update(self, ip):
        endpoint = "/update"
        data = {
            "ip": ip,
            "files": folderinfo.getfolderinfo(self.folderpath, self.root_uri)
        }
        json_data = json.dumps(data)
        print(json_data)
        response = self.post(endpoint=self.server+endpoint,
                             data=json_data)
        self.parse_response(response.text)

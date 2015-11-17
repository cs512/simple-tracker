#!/usr/bin/env python
# coding=utf-8

from flask import request, Flask
from db.models import File, Client
import db, json
import traceback


class Server:

    JSON_HEADER = {'Content-Type': 'application/json'}

    def __init__(self, ctl_port):
        self.web_app = Flask(__name__)
        self.ctl_port = ctl_port
        self.web_app.add_url_rule('/', 'index', self.index, methods=['GET', 'POST'])
        self.web_app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.web_app.add_url_rule('/deregister', 'deregister', self.deregister, methods=['DELETE'])
        self.web_app.add_url_rule('/update', 'update', self.update, methods=['POST'])
        self.web_app.add_url_rule('/transfer', 'transfer', self.transfer, methods=['POST'])
        self.web_app.add_url_rule('/file/<sha>', 'find_file', self.find_file, methods=['GET'])
        self.web_app.add_url_rule('/heartbeat', 'heartbeat', self.heartbeat, methods=['POST'])
        self.web_app.register_error_handler(405, self.bad_method)
        self.db = db.Database()

    def run(self):
        self.web_app.run(host="0.0.0.0", port=self.ctl_port)

    def bad_method(self, error = None):
        return '{"status":"ERROR_METHOD_NOT_ALLOWED"}', 405, Server.JSON_HEADER

    def bad_request(self, error = None, msg = ""):
        return '{"status":"ERROR_BAD_REQUEST","msg":"' + msg + '"}', 400, Server.JSON_HEADER

    def forbidden(self, error = None):
        return '{"status":"ERROR_FORBIDDEN"}', 403, Server.JSON_HEADER

    def success(self):
        return '{"status":"OK"}', 200, Server.JSON_HEADER

    def index(self):
        if request.method == 'POST':
            return '{"json":"test_post"}', 200, Server.JSON_HEADER
        else:
            return '{"json":"test_get"}', 200, Server.JSON_HEADER

    def register(self):
        json_dict = request.get_json()
        try:
            client = Client(json_dict)
            if self.db.add_client(client):
                return self.success()
            else:
                return self.bad_request(msg="Client Exist")
        except Exception, e:
            print(traceback.print_exc())
            return self.bad_request(msg="JSON Error")

    def deregister(self):
        json_dict = request.get_json()
        try:
            if self.db.delete_client(json_dict['ip']):
                return self.success()
            else:
                return self.bad_request(msg="Client Not Exist")
        except Exception, e:
            print(traceback.print_exc())
            return self.bad_request(msg="JSON Error")

    def update(self):
        json_dict = request.get_json()
        print(json_dict['ip'])
        try:
            client = self.db.get_client(json_dict['ip'])
            files = []
            for each_file in json_dict['files']:
                file_obj = File(each_file)
                files.append(file_obj)
            if self.db.update_files(client, files):
                return self.success()
            else:
                return self.bad_request(msg="Client Not Exist")
        except Exception, e:
            print(traceback.print_exc())
            return self.bad_request(msg="JSON Error")

    def transfer(self):
        pass

    def find_file(self, sha):
        try:
            files = self.db.get_files(str(sha).lower())
            output = {}
            output[sha] = []
            for each_client, each_file in files:
                file_dic = {}
                file_dic['ip'] = each_client.ip
                file_dic['uri'] = each_file.uri
                file_dic['size'] = each_file.size
                output[sha].append(file_dic)
            return json.dumps(output), 200, Server.JSON_HEADER
        except Exception, e:
            print(traceback.print_exc())
            return self.bad_request(msg="JSON Error")

    def heartbeat(self):
        try:
            json_dic = request.get_json()
            if self.db.renew(json_dic['ip']):
                return self.success()
            else:
                return self.bad_request(msg='Client Not Exist')
        except Exception, e:
            print(traceback.print_exc())
            return self.bad_request(msg="JSON Error")

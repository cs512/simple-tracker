#!/usr/bin/env python

from simpletrackerclient import STClientInstance
from simplewatchdog import SimpleWatchDog
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from flask import request, Flask
import threading
import os

ROUTES = []


class MyHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        # default root -> cwd
        root = os.getcwd()
        # look up routes and get root directory
        for patt, rootDir in ROUTES:
            if path.startswith(patt):
                #print("patt:" + patt)
                #print("rootDir" + rootDir)
                path = path[len(patt):]
                root = rootDir
                break
        # new path
        return os.path.join(root, path)


class clientmain:

    JSON_HEADER = {'Content-Type': 'application/json'}

    def __init__(self,
                 server_ip,
                 server_port,
                 local_ip,
                 local_folder_path,
                 local_ctl_port,
                 local_trans_port):

        self.server_ip = server_ip  # 192.168.1.10
        self.server_port = server_port  # 8000
        self.local_ip = local_ip  # 192.168.1.15
        self.local_folder_path = local_folder_path  # /home/shaw/Develop/snlab/simple-tracker/client
        self.local_ctl_port = local_ctl_port  # 8000
        self.local_trans_port = local_trans_port  # 9000
        self.stc = STClientInstance(
            'http://'+self.server_ip+':'+str(self.server_port),
            self.local_folder_path,
            'http://'+self.local_ip+':'+str(self.local_trans_port)
        )
        self.swd = SimpleWatchDog(self.local_folder_path, self.stc, self.local_ip)
        self.web_app = Flask(__name__)
        self.web_app.add_url_rule('/transfer', 'transfer', self.transfer, methods=["post"])
        self.threads = []

    def success(self):
        return '{"status":"OK"}', 200, clientmain.JSON_HEADER

    def run(self):
        self.stc.register(self.local_ip, str(self.local_ctl_port))
        self.stc.update(self.local_ip)
        t1 = threading.Thread(target=self.start_HTTPServer)
        t2 = threading.Thread(target=self.start_simplewatchdog)
        t3 = threading.Thread(target=self.start_flask_server)
        self.threads.append(t1)
        self.threads.append(t2)
        self.threads.append(t3)
        for t in self.threads:
            t.setDaemon(True)
            t.start()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.stc.deregister(self.local_ip)

    def start_HTTPServer(self):
        global ROUTES
        ROUTES.append(('/', self.local_folder_path))
        httpd = HTTPServer(('127.0.0.1', self.local_trans_port), MyHandler)
        httpd.serve_forever()
        print("start HTTPServer")

    def start_simplewatchdog(self):
        self.swd.start()
        print("start simplewatchdog")

    def transfer(self):
        print("I received transfer message")
        return self.success()

    def start_flask_server(self):
        self.web_app.run(host="0.0.0.0", port=self.local_ctl_port)




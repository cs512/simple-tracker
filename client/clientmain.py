#!/usr/bin/env python

from simpletrackerclient import STClientInstance
from simplewatchdog import SimpleWatchDog
import threading
import os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

ROUTES = []


class MyHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # default root -> cwd
        root = os.getcwd()

        # look up routes and get root directory
        for patt, rootDir in ROUTES:
            if path.startswith(patt):
                print("patt:" + patt)
                print("rootDir" + rootDir)
                path = path[len(patt):]
                root = rootDir
                break
        # new path
        return os.path.join(root, path)

class clientmain:

    def __init__(self, server_ip, local_ip, local_folder_path, ctl_port, trans_port):
        self.server_ip = server_ip  # 192.168.1.10
        self.local_ip = local_ip  # 192.168.1.15
        self.local_folder_path = local_folder_path  # /home/shaw/Develop/snlab/simple-tracker/client
        self.ctl_port = ctl_port  # 8000
        self.trans_port = trans_port  # 9000
        self.stc = STClientInstance(
            'http://'+self.server_ip+':8000',
            self.local_folder_path,
            'http://'+self.local_ip+':'+str(self.trans_port)
        )
        self.swd = SimpleWatchDog(self.local_folder_path, self.stc, self.local_ip)
        self.threads = []

    def run(self):
        self.stc.register(self.local_ip, self.ctl_port)
        self.stc.update(self.local_ip)
        t1 = threading.Thread(target=self.start_HTTPServer)
        t2 = threading.Thread(target=self.start_simplewatchdog)
        self.threads.append(t2)
        self.threads.append(t1)
        t2.setDaemon(True)
        t1.setDaemon(True)
        t2.start()
        t1.start()

    def start_HTTPServer(self):
        global ROUTES
        ROUTES.append(('/', self.local_folder_path))
        httpd = HTTPServer(('127.0.0.1', self.trans_port), MyHandler)
        httpd.serve_forever()
            #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            #httpd = SocketServer.TCPServer(("", self.trans_port), Handler)
            #print "serving at port", self.trans_port
            #httpd.serve_forever()

    def start_simplewatchdog(self):
        self.swd.start()

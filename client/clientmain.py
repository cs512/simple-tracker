#!/usr/bin/env python

from simpletrackerclient import STClientInstance
from simplewatchdog import SimpleWatchDog

class clientmain:

    def __init__(self, server_ip, local_ip, local_folder_path, ctl_port, trans_port):
        self.server_ip = server_ip  # 192.168.1.10
        self.local_ip = local_ip  # 192.168.1.15
        self.local_folder_path = local_folder_path  # /home/shaw/Develop/snlab/simple-tracker/client
        self.ctl_port = ctl_port  # 8000
        self.trans_port = trans_port  # 9000

    def run(self):
        stc = STClientInstance(
            'http://'+self.server_ip+':8000',
            self.local_folder_path,
            'http://'+self.local_ip+':'+self.ctl_port
        )
        swd = SimpleWatchDog(self.local_folder_path, stc, self.local_ip)

        stc.register(self.local_ip, self.ctl_port)
        stc.update(self.local_ip)

        swd.start();

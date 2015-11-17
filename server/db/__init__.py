#!/usr/bin/env python
# coding=utf-8
import time, threading, copy


class Database:

    def __init__(self):
        # IP Address -> client,SHA->files
        self.client_table = {}
        self.mutex = threading.Lock()
        self.thread = threading.Thread(target=self.check_clients)
        self.thread.daemon = True
        self.thread.start()

    def add_client(self, client):
        if not self.mutex.acquire(10):
            return False
        if client.ip in self.client_table:
            self.mutex.release()
            return False
        self.client_table[client.ip] = {}
        self.client_table[client.ip]['client'] = client
        self.client_table[client.ip]['files'] = {}
        self.client_table[client.ip]['time'] = time.time()
        self.mutex.release()
        return True

    def get_client(self, ip):
        if not self.mutex.acquire(10):
            return None
        ip = str(ip)
        if ip in self.client_table:
            output = copy.deepcopy(self.client_table[ip]['client'])
            self.mutex.release()
            return output
        else:
            self.mutex.release()
            return None

    def delete_client(self, ip):
        if not self.mutex.acquire(10):
            return False
        if ip in self.client_table:
            self.client_table.pop(ip)
            self.mutex.release()
            return True
        else:
            self.mutex.release()
            return False

    def update_files(self, client, files):
        if not self.mutex.acquire(10):
            return False
        if client.ip in self.client_table:
            self.client_table[client.ip] = {}
            self.client_table[client.ip]['client'] = client
            self.client_table[client.ip]['files'] = {}
            self.client_table[client.ip]['time'] = time.time()
            for each_file in files:
                self.client_table[client.ip]['files'][each_file.sha] = each_file
            self.mutex.release()
            return True
        else:
            self.mutex.release()
            return False

    def get_files(self, sha):
        if not self.mutex.acquire(10):
            return []
        output = []
        sha = sha.lower()
        for each_client_ip in self.client_table:
            if sha in self.client_table[each_client_ip]['files']:
                output.append((self.client_table[each_client_ip]['client'],
                               self.client_table[each_client_ip]['files'][sha]))
        self.mutex.release()
        return output

    def renew(self, ip):
        if not self.mutex.acquire(10):
            return False
        if ip in self.client_table:
            self.client_table[ip]['time'] = time.time()
            self.mutex.release()
            return self.client_table[ip]
        else:
            self.mutex.release()
            return False

    def check_clients(self):
        while True:
            if not self.mutex.acquire(10):
                return
            time_now = time.time()
            for each_ip in self.client_table:
                if time_now - self.client_table[each_ip]['time'] > 600:
                    self.delete_client(each_ip)
            self.mutex.release()
            time.sleep(60)

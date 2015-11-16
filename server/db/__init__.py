#!/usr/bin/env python
# coding=utf-8

class Database:

    def __init__(self):
        # IP Address -> client,SHA->files
        self.client_table = {}

    def add_client(self, client):
        if client.ip in self.client_table:
            return None
        self.client_table[client.ip] = {}
        self.client_table[client.ip]['client'] = client
        self.client_table[client.ip]['files'] = {}
        return self.client_table[client.ip]

    def get_client(self, ip):
        ip = str(ip)
        if ip in self.client_table:
            return self.client_table[ip]['client']
        else:
            return None

    def delete_client(self, ip):
        if ip in self.client_table:
            return self.client_table.pop(ip)
        else:
            return None

    def update_files(self, client, files):
        if client.ip in self.client_table:
            self.client_table[client.ip] = {}
            self.client_table[client.ip]['client'] = client
            self.client_table[client.ip]['files'] = {}
            for each_file in files:
                self.client_table[client.ip]['files'][each_file.sha] = each_file
        else:
            return None

    def get_files(self, sha):
        output = []
        sha = sha.lower()
        for each_client_ip in self.client_table:
            if sha in self.client_table[each_client_ip]['files']:
                output.append((self.client_table[each_client_ip]['client'],
                               self.client_table[each_client_ip]['files'][sha]))
        return output

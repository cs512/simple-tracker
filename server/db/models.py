#!/usr/bin/env python
# coding=utf-8


class File:

    def __init__(self, json_dic):
        self.sha = str(json_dic['sha']).lower()
        self.uri = str(json_dic['uri'])
        self.size = int(json_dic['size'])


class Client:

    def __init__(self, json_dic):
        self.ip = str(json_dic['ip'])
        self.ctl_port = int(json_dic['ctl_port'])

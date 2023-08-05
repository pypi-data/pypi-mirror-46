#!/usr/bin/python

import connection
import functions
import influxdb

class IosClient:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_binding_by_ip(self, ipaddress):
        data = functions.get_binding_by_ip(ipaddress, self.host, self.username, self.password)
        return data

    def get_cpu_load(self):
        data = connection.get_cpu_load(self.host, self.username, self.password, self.port)
        return data


class InfluxPush:
    def __init__(self, url):
        self.url = url

    def push_to_influxdb(self, datapath, value):
        influxdb.push_data(self.url, datapath, value)


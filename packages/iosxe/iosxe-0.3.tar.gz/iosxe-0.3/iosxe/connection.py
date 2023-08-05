#!/usr/bin/python
import paramiko, time
from ncclient import manager
import re

def csr_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           device_params={'name': "csr"},
                           timeout=30
            )


def get_cpu_load(host,user,password,port):
    data = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('show platform resources')
    data = stdout.read() + stderr.read()
    client.close()
    a1 = re.search(r'Control Processor\s{2,100}(\d{1,4}.\d{0,4})%\s', data)
    val = a1.group(1)
    return val

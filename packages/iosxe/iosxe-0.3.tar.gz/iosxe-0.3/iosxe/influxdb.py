import requests


def push_data(url, datapath, val):
    data11 = datapath + str(val)
    requests.post(url, data11)


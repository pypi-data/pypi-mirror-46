# -*- coding:utf-8 -*-


import requests
import json


class Docker(object):
    def __init__(self):
        pass

    @staticmethod
    def query_vessel():
        url = "http://localhost:2375/containers/json?all=1"
        r = requests.get(url)
        decoded = json.loads(r.text)

        for i in decoded[0]:
            print(i, decoded[0].get(i))

    @staticmethod
    def warehouse():
        url = "http://localhost:5000/v2/_catalog"
        r = requests.get(url)
        decoded = json.loads(r.text)
        return decoded


if __name__ == '__main__':
    docker = Docker()
    docker.query_vessel()
    print()
    print(docker.warehouse())

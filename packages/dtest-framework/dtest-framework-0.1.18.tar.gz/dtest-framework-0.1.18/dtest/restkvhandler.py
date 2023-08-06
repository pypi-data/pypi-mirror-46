from .handler import KvHandler
import requests
import json


class RESTKvHandler(KvHandler):

    def __init__(self, apiUrl, retrievePath, publishPath):
        self.url = apiUrl
        self.retrPath = retrievePath
        self.pubPath = publishPath

    def retrieve(self, key):
        resp = requests.get('http://' + self.url + self.retrPath + key)
        if resp.status_code != 200:
            raise ConnectionError(
                'GET ' + self.retrPath + ' {}'.format(resp.status_code))
        return resp.json()

    def publish(self, key, value):
        resp = requests.post('http://' + self.url +
                             self.pubPath, json={"key": key, "value": value})
        if resp.status_code != 200:
            raise ConnectionError('POST ' + self.pubPath +
                                  ' {}'.format(resp.status_code))
        return True

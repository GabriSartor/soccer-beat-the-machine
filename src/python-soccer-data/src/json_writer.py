import json
import os

class JSonWR(object):
    def save_json(self, data, name):
        fileName = '_'.join(name)
        print('Creating json: {}'.format(fileName))
        jsonFile = open('data/{}'.format(fileName), 'w')
        if jsonFile:
            json.dump(data, jsonFile)

    def open_json(self, name):
        fileName = '_'.join(name)
        print('Opening json: {}'.format(fileName))
        jsonFile = open('data/{}'.format(fileName), 'r')
        if jsonFile:
            return json.load(jsonFile)
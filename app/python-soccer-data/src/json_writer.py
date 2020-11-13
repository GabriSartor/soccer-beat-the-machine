import json
import os
import errno

class JSonWR(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def save_json(self, data, name):
        fileName = '_'.join(name)
        print('Creating json: {}'.format(fileName))
        jsonFile = open('{}/{}.json'.format(self.path, fileName), 'w')
        if jsonFile:
            json.dump(data, jsonFile)

    def open_json(self, name):
        fileName = '_'.join(name)
        print('Opening json: {}'.format(fileName))
        jsonFile = open('{}/{}.json'.format(self.path, fileName), 'r')
        if jsonFile:
            return json.load(jsonFile)
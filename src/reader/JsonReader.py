import json as jsn


class JsonReader(object):
    def read(self, path='configs/config.json'):
        config = self._read(path=path)
        return config

    def _read(self, path):
        with open(path, 'r+') as json_file:
            json = jsn.loads(json_file.read())
        return json

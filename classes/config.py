import json
from _global import *
from os.path import join


class Config:

    @staticmethod
    def readConfiguration():
        config = {}
        with open(CONFIG_PATH) as _config:
            config = json.load(_config)
        return config

    @staticmethod
    def get(key):
        _json = Config.readConfiguration()
        if key not in _json.keys():
            err(f'Key "{key}" not found in configuration file')
        return _json[key]

    @staticmethod
    def writeConfiguration(configuration):
        success = False
        with open(join(SCRIPT_PATH, 'config', 'config.json'), 'w') as _config:
            try:
                json.dump(configuration, _config, indent=4)
                success = True
            except Exception as e:
                success = False
        return success

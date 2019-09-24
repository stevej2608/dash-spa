import os
import json


def read_config(config=None):
    if config is None:
        config = os.environ['DASH_SPA_ENV'] if 'DASH_SPA_ENV' in os.environ else 'default'
    file_path = 'config/{}.json'.format(config)
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    except Exception:
        return {}

# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object

class Config(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Config(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Config(b) if isinstance(b, dict) else b)

def get(conf):
    conf = conf.split('.')
    config = _config
    for c in conf:
        if c in config:
            config = config[c]
        else:
            config = {}
    obj = Config(config)
    return obj

_config = read_config()

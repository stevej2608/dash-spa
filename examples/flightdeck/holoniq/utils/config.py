import os
import sys

def read_config(config=None):
    """Read and return the requested configuration object

    The supplied config name is the prefix for the name of
    a configuration class that the function expects to find in
    the settings.py module. For example 'test' will resolve to a
    class named `testConfig`.

    If the config argument is upper case it is assumed to refere to
    an environmental variable. The environmental variables value will
    be used as the prefix.

    If no config name is supplied or the defined environmental variable
    does not exist an attempt is made to return a 'default' 
    configuration class defaultConfig.


    Keyword Arguments:
        config {str} -- The config prefix, test, default, prod, FLASK_ENV

    Returns:
        obj -- The requested configuration
    """

    if config is None:
        config = os.environ['FLASK_ENV'] if 'FLASK_ENV' in os.environ else 'default'

    class_name = config.capitalize() + 'Config'

    try:
        module = __import__('settings')
        class_ = getattr(module, class_name)
        instance = class_()
        return instance
    except Exception as ex:
        print(f' * Error, unable to resolve configuration: {config}, {ex}')
        sys.exit()

CONFIG = read_config()

# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object

class Config(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Config(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Config(b) if isinstance(b, dict) else b)


def get(conf, config=CONFIG):
    """Return the sub-config of the given main config

    Arguments:
        conf {str} -- nested config reference

    Keyword Arguments:
        config {obj} -- The master config (default: {CONFIG})

    Returns:
        obj -- the sub-config
    """

    conf = conf.split('.')

    for c in conf:
        if hasattr(config, c):
            config = getattr(config, c)
        elif c in config:
            config = config[c]
        else:
            config = {}

    obj = Config(config)
    return obj

import os
import pytest
from dash_spa.spa_config import read_config

def get_config(file):
    """Load module relative config file"""
    module = __name__.split('.')[-1]
    file = __file__.replace(f"{module}.py", file)
    return read_config(file)

def test_config_simple():

    # This should fail as env SPA_PASSWORD is not defined

    with pytest.raises(Exception):
        get_config('test.ini')

    # Try again ...

    os.environ["SPA_PASSWORD"] = "secret"

    config = get_config('test.ini')
    options = config.get('options')

    assert options.email == 'bigjoe@gmail.com'
    assert options.password == 'secret'


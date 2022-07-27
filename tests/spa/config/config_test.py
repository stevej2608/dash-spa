import os
import pytest
from dash_spa.spa_config import read_config, ConfigurationError

def get_config(file):
    """Load module relative config file"""
    module = __name__.split('.')[-1]
    file = __file__.replace(f"{module}.py", file)
    return read_config(file)

def test_config_simple():
    """
    Test that environmental variable reference in the
    configuration file './test.ini' is handled correctly.
    """

    # This should fail as environmental variable SPA_ADMIN_PASSWORD is not defined

    with pytest.raises(ConfigurationError) as error:
        get_config('test.ini')

    assert 'ENV variable "SPA_ADMIN_PASSWORD" is not assigned' in str(error)

    # Define SPA_ADMIN_PASSWORD and try again ...

    os.environ["SPA_ADMIN_PASSWORD"] = "secret"

    config = get_config('test.ini')
    assert config

    # read 'admin' config

    admin = config.get('admin')

    assert admin
    assert admin.email == 'bigjoe@gmail.com'
    assert admin.password == 'secret'

    # Try to access a nonexistent section

    with pytest.raises(ConfigurationError) as error:
        admin = config.get('users')

    assert 'Section users has not been defined' in str(error)

    # Try to access a nonexistent attribute

    assert admin.undefined == None

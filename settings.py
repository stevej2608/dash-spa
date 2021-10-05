class DefaultConfig(object):
    """Base configuration."""

    flask = {
        "SECRET_KEY": "my secret flask password",
        "URL_PREFIX": "api"
    }

    logging = {"level": "INFO"}

    user_db = {
        "database_uri": "sqlite:///db.sqlite"
    }
    mail_options = {
        "sender": "admin@joes.com",
        "active": "gmail",
        "gmail": {
            "host": "smtp.gmail.com",
            "port": 465,
            "secure": True,
            "auth": {
                "user": "bigjoe@gmail.com",
                "password": "bigjoepassword"
            }
        },
        "plusnet": {
            "host": "relay.plus.net",
            "port": 587,
            "secure": False,
            "auth": {
                "user": "bigjoe",
                "password": "bigjoesotherpassword"
            }
        }
    }


class ProdConfig(DefaultConfig):
    """Production configuration."""


class DevConfig(DefaultConfig):
    """Development configuration."""


class TestConfig(DefaultConfig):
    """Test configuration."""

    flask = {
        "SECRET_KEY": "my secret flask password",
        "URL_PREFIX": "api",
        "FLASK_ENV" : "test"
    }

    user_db = {
        "database_uri": "sqlite:///tests/admin/test_db.sqlite"
    }

    logging = {"level": "WARN"}

import os
import logging

class BaseConfig(object):
    DEBUG = False
    logging.getLogger("flask_ask").setLevel(logging.DEBUG)

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    logging.getLogger("flask_ask").setLevel(logging.DEBUG)
    #ASK_APPLICATION_ID = "<add-your-application-id-here>"

class TestingConfig(BaseConfig):
    DEBUG = True
    logging.getLogger("flask_ask").setLevel(logging.DEBUG)
    ASK_VERIFY_REQUESTS = False # Don't verify whether the requests are from Alexa service


config = {
    "development": "goodbooks_config.DevelopmentConfig",
    "testing": "goodbooks_config.TestingConfig",
    "default": "goodbooks_config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])

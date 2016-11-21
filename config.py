import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////dev/TP/server/balon.sqlite3'

    # DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    DATABASE = "C:\dev\TP\server\\balooooooon.sqlite3"
    USERNAME = 'admin',
    PASSWORD = 'admin'

    LOGGING_LOGGER = "Balon Logger"
    LOGGING_LOGGER_DB = "DB Logger"

    LOGGING_FORMAT = '%(asctime)s - %(name)s [%(levelname)s] %(module)s.%(funcName)s(): %(message)s'
    LOGGING_LOCATION = 'balooooooon.log'
    LOGGING_LEVEL = logging.DEBUG

    LOGGING_CONSOLE = True
    LOGGING_LEVEL_CONSOLE = logging.DEBUG
    # DEBUG, INFO, WARNING, ERROR, CRITICAL


class ProductionConfig(Config):
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////users.sqlite3'
    LOGGING_LOCATION = "/var/log/flask/balon.log"
    LOGGING_LEVEL = logging.ERROR

    LOGGING_CONSOLE = False

    APP_AUTHENTICATE_FLIGHT = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    NO_DB = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True

    APP_AUTHENTICATE_FLIGHT = False

class TestingConfig(Config):
    TESTING = True
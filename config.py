import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////users.sqlite3'

    LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] %(module)s.%(funcName)s(): %(message)s'
    LOGGING_LOCATION = 'balooooooon.log'
    LOGGING_LEVEL = logging.DEBUG
    # DEBUG, INFO, WARNING, ERROR, CRITICAL


class ProductionConfig(Config):
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////users.sqlite3'
    LOGGING_LOCATION = "/var/log/flask/balon.log"
    LOGGING_LEVEL = logging.WARNING


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    NO_DB = True

class TestingConfig(Config):
    TESTING = True
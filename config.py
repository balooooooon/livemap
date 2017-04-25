import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

# ---------------------------------------------
#      Default Config
# ---------------------------------------------
class Config(object):
    DEBUG = False
    TESTING = False
    REMOTE = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    
    SQLALCHEMY_DATABASE_URI = 'mysql://balon:balon@localhost/balon_dev'


    MYSQL_DATABASE_USER = "balon"
    MYSQL_DATABASE_PASSWORD = "balon"
    MYSQL_DATABASE_DB = "balon_dev"
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_CURSORCLASS = "SSDictCursor"


    LOGGING_LOGGER = "Balon Logger"
    LOGGING_LOGGER_DB = "DB Logger"
    LOGGING_LOGGER_API = "API Logger"

    LOGGING_FORMAT = '%(asctime)s - %(name)s [%(levelname)s] %(module)s.%(funcName)s(): %(message)s'
    LOGGING_LOCATION = 'balooooooon.log'
    LOGGING_LEVEL = logging.DEBUG

    LOGGING_CONSOLE = True
    LOGGING_CONSOLE_DB = True
    LOGGING_LEVEL_CONSOLE = logging.DEBUG
    # DEBUG, INFO, WARNING, ERROR, CRITICAL

    
    TWITTER_CONSUMER_KEY = "VALUE"
    TWITTER_CONSUMER_SECRET = "VALUE"
    TWITTER_ACCESS_TOKEN = "VALUE"
    TWITTER_ACCESS_TOKEN_SECRET = "VALUE"

    FACEBOOK_PAGE_ID = "VALUE"
    FACEBOOK_ACCESS_TOKEN = "VALUE"

# ---------------------------------------------
#      Develop Server Config
# ---------------------------------------------
class DevelopConfig(Config):
    DEBUG = True
    TESTING = False
    REMOTE = True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

    # -- DATABASE 
    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://balon:balon@localhost/balon_dev'

    MYSQL_DATABASE_USER = "balon"
    MYSQL_DATABASE_PASSWORD = "balon"
    MYSQL_DATABASE_DB = "balon_dev"
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_CURSORCLASS = "SSDictCursor"

    # -- LOGGERS
    LOGGING_LOCATION = "/var/log/balon/dev/balon.log"
    LOGGING_LEVEL = logging.DEBUG

    LOGGING_CONSOLE = True
    LOGGING_CONSOLE_DB = True
    LOGGING_LEVEL_CONSOLE = logging.DEBUG
    # DEBUG, INFO, WARNING, ERROR, CRITICAL

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False

    APP_AUTHENTICATE_FLIGHT = False

# ---------------------------------------------
#      Production Server Config 
# ---------------------------------------------
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    REMOTE = True
    PRODUCTION = True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

    # -- DATABASE
    

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://balon:balon@localhost/balon_live'
    
    MYSQL_DATABASE_USER = "balon"
    MYSQL_DATABASE_PASSWORD = "balon"
    MYSQL_DATABASE_DB = "balon_live"
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_CURSORCLASS = "SSDictCursor"


    # -- LOGGERS
    LOGGING_LOCATION = "/var/log/balon/prod/balon.log"
    LOGGING_LEVEL = logging.ERROR

    LOGGING_CONSOLE = False
    LOGGING_CONSOLE_DB = False
    LOGGING_LEVEL_CONSOLE = logging.ERROR
    # DEBUG, INFO, WARNING, ERROR, CRITICAL


    APP_AUTHENTICATE_FLIGHT = True

# ---------------------------------------------
#      Config for developing on localhost
# ---------------------------------------------
class LocalConfig(Config):
    # DEVELOPMENT = True
    DEBUG = True
    # NO_DB = True

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True

    APP_AUTHENTICATE_FLIGHT = False

# ---------------------------------------------
#      Config for testing
# ---------------------------------------------
class TestingConfig(Config):
    TESTING = True

    # -- DATABASE
    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://balon:balon@localhost/balon_test'
    
    MYSQL_DATABASE_USER = "balon"
    MYSQL_DATABASE_PASSWORD = "balon"
    MYSQL_DATABASE_DB = "balon_test"
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_CURSORCLASS = "SSDictCursor"
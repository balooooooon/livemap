# ----------------- IMPORTS -----------------

# Flask imports
import MySQLdb
from flask import Flask
from flask_socketio import SocketIO
import logging
from balon.controller.BalloonObserver import BalloonObserver

# ----------------- IMPORTS -----------------

app = Flask(__name__)

# http://stackoverflow.com/questions/15603240/flask-how-to-manage-different-environment-databases
# Nacita config zo suboru config.py

if app.config["TESTING"]:
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopConfig')

# Ak je vytvorena premenna prostredia BALLOON_CONFIG, prepise config vyssie
app.config.from_envvar('BALLOON_CONFIG', silent=True)

# --- Configure logging ---

# app.logger = logging.getLogger("My Logger")
LOG = logging.getLogger(app.config['LOGGING_LOGGER'])

handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setLevel(app.config['LOGGING_LEVEL'])
handler.setFormatter(formatter)
# app.logger.addHandler(handler)
LOG.addHandler(handler)

if (app.config['LOGGING_CONSOLE']):
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(app.config['LOGGING_LEVEL_CONSOLE'])
    streamHandler.setFormatter(formatter)
    # app.logger.addHandler(streamHandler)
    LOG.addHandler(streamHandler)

# app.logger.propagate = False

LOG.setLevel(logging.DEBUG)


async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

LOG.debug("Starting flask app __init__.py")

from balon.database import DBConnector
DBConnector.connect_db(app)

# TODO Test Database connection
# --- Observer initialization
observer = BalloonObserver()

from balon.controller.SocialController import SocialController

socialController = SocialController()
observer.register(socialController)

from balon.controller.SocketController import SocketController

socketController = SocketController()
observer.register(socketController)

import main


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    socketio.run(app)

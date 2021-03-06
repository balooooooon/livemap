# ----------------- IMPORTS -----------------

# Flask imports
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import logging

# ----------------- IMPORTS -----------------

app = Flask(__name__)

# http://stackoverflow.com/questions/15603240/flask-how-to-manage-different-environment-databases
# Nacita config zo suboru config.py
app.config.from_object('config.ProductionConfig')

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

# LOG.debug("Database Path: %s", app.config["DATABASE"])

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

LOG.debug("Starting flask app __init__.py")

db = SQLAlchemy(app)

import main

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    socketio.run(app)

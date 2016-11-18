# ----------------- IMPORTS -----------------

# Flask imports
from flask import Flask
from flask_socketio import SocketIO
import logging

# ----------------- IMPORTS -----------------

app = Flask(__name__)

# import sys
# path = "/var/www/balon/" + __name__ + "/"
# print path
# sys.path.insert(0,path)

# sys.path.insert(0,"C:\\dev\\TP\\server\\balon")

# http://stackoverflow.com/questions/15603240/flask-how-to-manage-different-environment-databases
# Nacita config zo suboru config.py
app.config.from_object('config.DevelopmentConfig')

# Ak je vytvorena premenna prostredia BALLOON_CONFIG, prepise config vyssie
app.config.from_envvar('BALLOON_CONFIG', silent=True)

# Configure logging
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)


app.logger.info("Database Path: %s", app.config["DATABASE"])

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


db = None

import main
import balon.database.DBConnector
#TODO Test Database connection

if (app.config["DEBUG"]):
    print "DB_PATH: %s", app.config["DATABASE"]
    print("Starting flask app __init__.py")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    socketio.run(app)

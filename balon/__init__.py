# ----------------- IMPORTS -----------------

# Flask imports
from flask import Flask, current_app
from flask_socketio import SocketIO


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

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

import main

if (app.config["DEBUG"]):
    print("Starting flask app __init__.py")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    socketio.run(app)

# ----------------- IMPORTS -----------------

# Flask imports
from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

import random
import json

# Controller
from controller import Controller

# ----------------- IMPORTS -----------------


app = Flask(__name__)

print "DEBUG"
print __name__

# import sys
# sys.path.insert(0,"C:\\dev\\TP\\server\\balon")

# http://stackoverflow.com/questions/15603240/flask-how-to-manage-different-environment-databases
# Nacita config zo suboru config.py
app.config.from_object('config.DevelopmentConfig')

# Ak je vytvorena premenna prostredia BALLOON_CONFIG, prepise config vyssie
app.config.from_envvar('BALLOON_CONFIG', silent=True)

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

with app.app_context():
    Controller.app = app

if (app.config["DEBUG"]):
    print("Starting flask app __init__.py")

if (app.config["DEBUG"]):
    print " -- Debug values: -- "
    print "getBalloonLocation:"
    print Controller.getBalloonLocation()
    print "getBalloonPath:"
    print Controller.getBalloonPath()
    print "getBalloonStart:"
    print Controller.getBalloonBurst()
    print "getBalloonBurst:"
    print Controller.getBalloonStart()
    print " -- Debug values  -- "

def debug():
    return app.config["DEBUG"]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/map')
def balloonDashboard():
    # balloonStatus =

    balloonLocation = Controller.getBalloonLocation()

    balloonPath = Controller.getBalloonPath()

    balloonBurst = Controller.getBalloonBurst()

    balloonStart = Controller.getBalloonStart()

    data = {
        'path': balloonPath,
        'location': balloonLocation,
        'burst': balloonBurst,
        'start': balloonStart
    }

    # balloonLanding = getBalloonLanding()

    # balloonTelemetry = getActualTelemetry()

    if (debug()):
        print "Sending data: "
        print data

    return render_template("index.html", async_mode=socketio.async_mode, balloon_data=data)


# ------ API -------

def authenticate(auth_hash):
    # TODO
    return False

# Deprecated
@app.route('/api/update', methods=['POST'])
def api_update():
    if request.method == 'POST':
        print("POST request")
        json_request = request.get_json(force=False, silent=False, cache=False)
        # TODO Not a JSON Exception

        if json_request.has_key("pass"):
            print "Has key"
            auth_hash = json_request["pass"]
            authenticated = authenticate(auth_hash)
            if (not authenticated):
                print "Not authenticated."
                return "Not authenticated.", 401
        else:
            print "Not authenticated."
            return "Not authenticated.", 401

        if json_request["type"] == "updateLocation":
            data = {}
            data["type"] = "baloonLocation"
            data["timestamp"] = json_request["data"]["timestamp"]
            data["location"] = {}
            data["location"]["lat"] = json_request["data"]["location"]["lat"]
            data["location"]["lng"] = json_request["data"]["location"]["lng"]
            json_data = json.dumps(data)
            socketio.emit("baloon_update", json_data, namespace="/map")
            return "Data updated."
    else:
        print("GET request")
        print(request)


@app.route('/api/dumb_json', methods=['POST'])
def api_dumbjson():
    if request.method == 'POST':
        print("POST request")
        json_request = json.dumps(request.get_json(force=False, silent=False, cache=False))
        print(json_request)
        socketio.emit("baloon_update", json_request, namespace="/map")
        return "Data sent."


# -------- SOCKETS ---------

@socketio.on('my_event', namespace='/socket/')
def sendMessage():
    emit('message', {'data': 'my data'})


@socketio.on('connect', namespace='/socket/')
def test_connect():
    print("Connected.")
    emit('message', {'data': 'Connected to Socket'})
    print("Message sent.")


thread = None


@socketio.on('connect', namespace='/map')
def baloonUpdate():
    print("Client connected");
    emit('message', {'data': 'Client connected'})
    global thread


# if thread is None:
# thread = socketio.start_background_task(target=background_thread)

messageType = ["baloonLocation", "baloonStart", "baloonBurst", "baloonLanding", "baloonPathUpdate"]


def background_thread():
    while True:
        socketio.sleep(5)
        i = random.randint(0, len(messageType) - 1)
        print("Sending " + messageType[i])
        socketio.emit('baloon_update', {'type': messageType[i]}, namespace="/map")


if __name__ == '__main__':
    socketio.run(app)

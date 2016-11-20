# ----------------- IMPORTS -----------------

# Flask imports
from datetime import datetime

from flask import Flask, render_template, request, url_for, current_app, jsonify, abort, redirect, flash
from flask_socketio import SocketIO, emit

import json

# Controller
from balon.controller import Controller, WebController
from balon import app, socketio

# ----------------- IMPORTS -----------------

print "Current_app"
print app.config["DEBUG"]

if app.config["DEBUG"]:
    print("Starting flask app main.py")

if app.config["DEBUG"]:
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

@app.route('/admin/flight')
def flight_administration():
    flights = Controller.getFlightAll()
    print flights
    return render_template("show_flights.html", flights=flights)

@app.route('/admin/flight/add', methods=['POST'])
def add_flight():
    if not request.method == 'POST':
        abort(405)

    if request.form['flightStartDate'] is not None and request.form['flightNumber'] is not None:
        # flash("Flight saved.")
        Controller.saveNewFlight(request.form['flightNumber'],request.form['flightStartDate'])
    else:
        app.logger.debug("Wrong input parameters for new Flight")

    return redirect(url_for('flight_administration'))

@app.route('/admin/flight/<int:flight_id>/detail')
def flight_detail(flight_id):

    flight = Controller.getFlightById(flight_id)

    parameters = None
    parameters = Controller.getParametersAllByFlight(flight_id)

    return render_template("show_flight_detail.html", parameters=parameters, flight=flight)

@app.template_filter('datetime')
def jinja2_filter_datetime(timestamp, format=None):
    DEFAULT_FORMAT = "%d.%m.%Y %H:%M:%S"
    date = datetime.fromtimestamp(timestamp)
    if format:
        return date.strftime(format)
    else:
        return date.strftime(DEFAULT_FORMAT)

# ------ API -------

@app.route('/api/dumb_json', methods=['POST'])
def api_dumbjson():
    if request.method == 'POST':
        print("POST request")
        json_request = json.dumps(request.get_json(force=False, silent=False, cache=False))
        print(json_request)
        socketio.emit("baloon_update", json_request, namespace="/map")
        return "Data sent."


@app.route('/api/mirror', methods=['POST'])
def api_mirror():
    if request.method == 'POST':
        app.logger.debug("API MIRROR: %s", jsonify(request.get_json(force=False, silent=False, cache=False)))
        return jsonify(request.get_json(force=False, silent=False, cache=False)), 202


@app.route('/api/test', methods=['GET', 'POST'])
def api_test():
    app.logger.debug("API TEST")
    return "TEST", 202


@app.route('/api/flight/<int:flight_number>/telemetry', methods=['POST'])
def api_telemetry(flight_number):
    if request.method != 'POST':
        abort(405)

    json_request = request.get_json(force=False, silent=False, cache=False)
    if not json_request.has_key("flightHash"):
        abort(400)

    flightHash = json_request["flightHash"]
    if not Controller.authenticate(flight_number, flightHash):
        abort(401)

    if json_request.has_key("data"):
        app.logger.info("Telemetry data accepted")
        # Controller.checkTelemetryJsonData(json_request["data"])
        Controller.saveNewTelemetry(flight_number, json_request["data"])
        # WebController.refreshSite(flight_number)


    return "OK", 201


@app.route('/api/flight/<int:flight_number>/event/<string:event>', methods=['POST'])
def api_events(flight_number, event):
    if request.method != 'POST':
        abort(405)

    if not Controller.isValidEvent(event):
        abort(400)

    json_request = request.get_json(force=False, silent=False, cache=False)
    if not json_request.has_key("flightHash"):
        abort(400)

    flightHash = json_request["flightHash"]
    if not Controller.authenticate(flight_number, flightHash):
        abort(401)

    if json_request.has_key("data"):
        # Controller.checkEventJsonData(json_request["data"])
        Controller.saveEvent(json_request["data"])
        WebController.refreshSite(flight_number)

    return "OK", 201


# -------- SOCKETS ---------

@socketio.on('my_event', namespace='/socket/')
def sendMessage():
    emit('message', {'data': 'my data'})


@socketio.on('connect', namespace='/socket/')
def test_connect():
    print("Connected.")
    emit('message', {'data': 'Connected to Socket'})
    print("Message sent.")


@socketio.on('connect', namespace='/map')
def balloonUpdate():
    app.logger.info("Client connected")
    print ("Client connected")
    emit('message', {'data': '[Server]: You have been connected.'})
    global thread

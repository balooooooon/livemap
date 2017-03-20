# ----------------- IMPORTS -----------------

# Flask imports
from datetime import datetime

from flask import Flask, render_template, request, url_for, current_app, jsonify, abort, redirect, flash
from flask_socketio import SocketIO, emit, join_room

import json

# Controller
from balon.controller import Controller# , WebController, SocialController
from balon import app, socketio, LOG,  db , observer

# ----------------- IMPORTS -----------------
from balon.models.Flight import Flight

LOG.debug("Starting flask app main.py")


@app.route('/map')
def balloonDashboard():
    # balloonStatus =

    # TODO Try/catch encode() and int()
    if request.args.has_key("flight"):
        num = request.args.get("flight")
        num = num.encode('ascii','ignore')
        if num.isdigit():
            flight_number = int(num)
            LOG.debug("Custom flight number: %d", flight_number)
        else:
            LOG.debug("Custom flight number: %d - Wrong variable", num)
            flight_number = 42
    else:
        flight_number = 42

    if Controller.flightExists(flight_number):
        # TODO Error message if Flight does not exists
        flight_number = 42

    data = {}

    balloonLocation = Controller.getBalloonLocation(flight_number)
    if balloonLocation:
        data['location'] = balloonLocation

    balloonPath = Controller.getBalloonPath(flight_number)
    if balloonPath:
        data['path'] = balloonPath

    balloonBurst = Controller.getBalloonBurst(flight_number)
    if balloonBurst:
        data['burst'] = balloonBurst

    balloonStart = Controller.getBalloonStart(flight_number)
    if balloonStart:
        data['start'] = balloonStart

    flightList = Controller.getFlightList()
    if flightList:
        data['flightList'] = flightList

    # balloonLanding = getBalloonLanding()

    # balloonTelemetry = getActualTelemetry()

    LOG.debug("Sending data: ", data)

    return render_template("index.html", async_mode=socketio.async_mode, balloon_data=data)


@app.route('/admin/flight')
def flight_administration():
    flights = Controller.getFlightAll()
    return render_template("show_flights.html", flights=flights)


@app.route('/admin/flight/add', methods=['POST'])
def add_flight():
    if not request.method == 'POST':
        abort(405)

    if request.form['flightStartDate'] is not None and request.form['flightNumber'] is not None:
        # flash("Flight saved.")
        Controller.saveNewFlight(request.form['flightNumber'], request.form['flightStartDate'])
    else:
        LOG.debug("Wrong input parameters for new Flight")

    return redirect(url_for('flight_administration'))


@app.route('/admin/flight/<int:flight_id>/delete')
def delete_flight(flight_id):
    abort(501)


@app.route('/admin/flight/<int:flight_id>/detail')
def flight_detail(flight_id):
    # TODO Change flight id to flight number
    flight = Controller.getFlightById(flight_id)

    parameters = None
    parameters = Controller.getParametersAllByFlight(flight_id)
    events = Controller.getEventsAllByFlight(flight_id)

    return render_template("show_flight_detail.html", parameters=parameters, flight=flight, events=events)


@app.template_filter('format_datetime')
def jinja2_filter_datetime(date, format=None):
    DEFAULT_FORMAT = "%d.%m.%Y %H:%M:%S"
    if format:
        return date.strftime(format)
    else:
        return date.strftime(DEFAULT_FORMAT)


@app.template_filter('from_timestamp')
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
        LOG.info("POST request")
        json_request = json.dumps(request.get_json(force=False, silent=False, cache=False))
        LOG.debug(json_request)
        socketio.emit("baloon_update", json_request, namespace="/map")
        return "Data sent."


@app.route('/api/mirror', methods=['POST'])
def api_mirror():
    if request.method == 'POST':
        # LOG.debug("API MIRROR: {}".format(request.get_json(force=False, silent=False, cache=False)))
        return jsonify(request.get_json(force=False, silent=False, cache=False))

@app.route('/api/test', methods=['GET', 'POST'])
def api_test():
    LOG.debug("API TEST")
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

    flight_id = Controller.getFlightByNumber(flight_number)

    if json_request.has_key("data"):
        LOG.info("Telemetry data accepted")
        # Controller.checkTelemetryJsonData(json_request["data"])
        Controller.saveNewParameters(flight_number, json_request["data"])
        observer.update(flight_id)
        # WebController.refreshSite(flight_number)
        # SocialController.postStatuses(altitude,timestamp)

    return "OK", 201


@app.route('/api/flight/<int:flight_number>/event/<string:event>', methods=['POST'])
def api_events(flight_number, event):
    if request.method != 'POST':
        abort(405)

    #if not Controller.isValidEvent(event):
    #    abort(400)

    json_request = request.get_json(force=False, silent=False, cache=False)
    if not json_request.has_key("flightHash"):
        abort(400)

    flightHash = json_request["flightHash"]
    if not Controller.authenticate(flight_number, flightHash):
        abort(401)

    flight_id = Controller.getFlightByNumber(flight_number)

    if json_request.has_key("data"):
        # Controller.checkEventJsonData(json_request["data"])
        Controller.saveNewEvent(flight_number,event,json_request["data"])
        observer.update(flight_id)
        # WebController.refreshSite(flight_number)

    return "OK", 201


# -------- SOCKETS ---------

@socketio.on('my_event', namespace='/socket/')
def sendMessage():
    emit('message', {'data': 'my data'})


@socketio.on('connect', namespace='/socket/')
def test_connect():
    LOG.info("Connected.")
    emit('message', {'data': 'Connected to Socket'})
    LOG.debug("Message sent.")


@socketio.on('connect', namespace='/map')
def balloonUpdate():
    LOG.info("Client connected")
    emit('message', {'data': '[Server]: You have been connected.'})
    global thread

@socketio.on('join', namespace='/map')
def socket_join(data):
    LOG.debug(data["flight"])
    flightNumber = data["flight"]
    flight_id = Controller.getFlightByNumber(flightNumber)
    join_room(flight_id)
    emit('message', {'data': 'Subscribed for flight #{}'.format(flightNumber)})

def init_db():
    from models import Flight, Parameter, Value, Event
    db.create_all()

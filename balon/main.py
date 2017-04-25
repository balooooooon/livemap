# ----------------- IMPORTS -----------------

# Flask imports
from datetime import datetime
from flask import Flask, render_template, request, url_for, current_app, jsonify, abort, redirect, flash
import json

# Controller
from balon.controller import Controller, WebController, PredictionController, SocialController
from balon import app, socketio, LOG, observer

# ----------------- IMPORTS -----------------

LOG.debug("Starting flask app main.py")


@app.route('/map')
def balloonDashboard():

    # Checks if flight number in URL, else use default number 42
    if request.args.has_key("flight"):
        num = request.args.get("flight")
        num = num.encode('ascii', 'ignore')
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

    flight = Controller.getFlightByNumber(flight_number);

    balloonLocation = Controller.getBalloonLocation(flight_number)
    if balloonLocation:
        data['location'] = balloonLocation

    # Get balloon flight path
    balloonPath = Controller.getBalloonPath(flight_number)
    if balloonPath:
        data['path'] = balloonPath

    # Get balloon burst location
    balloonBurst = Controller.getBalloonBurst(flight_number)
    if balloonBurst:
        data['burst'] = balloonBurst

    # Get balloon starting location
    balloonStart = Controller.getBalloonStart(flight_number)
    if balloonStart:
        data['start'] = balloonStart
        predictionResult, predictionPathResult = PredictionController.getBalloonLanding(data['start'])
        if predictionResult:
            data['landingPredicted'] = predictionResult
            data['predictedPath'] = predictionPathResult

    # Get list of all flights for drop-down selection
    flightList = Controller.getFlightList()
    if flightList:
        data['flightList'] = flightList

    # balloonLanding = getBalloonLanding()

    balloonTelemetry = Controller.getCurrentTelemetry(flight.id)
    if balloonTelemetry:
        LOG.debug(balloonTelemetry)
        data['telemetry'] = balloonTelemetry

    LOG.debug("Sending data: ", data)

    return render_template("index.html", async_mode=socketio.async_mode, balloon_data=data)


@app.route('/admin/flight')
def flight_administration():
    flights = Controller.getFlightAll()
    return render_template("show_flights.html", flights=flights)


@app.route('/admin/flight/add', methods=['POST'])
def xadd_flight():
    """
    @deprecated: Using REST API in newer version
    """
    if not request.method == 'POST':
        abort(405)

    if request.form['flightStartDate'] is not None and request.form['flightNumber'] is not None:
        # flash("Flight saved.")
        Controller.saveNewFlight(request.form['flightNumber'], request.form['flightStartDate'])
    else:
        LOG.debug("Wrong input parameters for new Flight")

    return redirect(url_for('flight_administration'))


@app.route('/admin/flight/<int:flight_id>/delete')
def xdelete_flight(flight_id):
    """
    @deprecated: Never really used
    """
    abort(501)


@app.route('/admin/flight/<int:flight_id>/detail')
def flight_detail(flight_id):
    # TODO Change flight id to flight number
    flight = Controller.getFlightById(flight_id)

    parameters = None
    parameters = Controller.getParametersAllByFlight(flight_id)

    charts = Controller.getChartTypes(flight_id)
    LOG.debug(charts)

    events = Controller.getEventsAllByFlight(flight_id)

    import json_tricks

    data = json_tricks.dumps(parameters, primitives=True)
    # LOG.debug(data)

    return render_template("show_flight_detail.html", parameters=parameters, flight=flight, events=events,
                           balloonData=data, chartData=charts)


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

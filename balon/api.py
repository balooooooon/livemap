import logging

from flask import abort, json, request, jsonify
from flask import make_response

from balon import app, socketio, observer
from balon.controller import Controller
from balon.models import Flight

LOG = logging.getLogger(app.config['LOGGING_LOGGER_API'])

handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setLevel(app.config['LOGGING_LEVEL'])
handler.setFormatter(formatter)
LOG.addHandler(handler)

if (app.config['LOGGING_CONSOLE']):
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(app.config['LOGGING_LEVEL_CONSOLE'])
    streamHandler.setFormatter(formatter)
    LOG.addHandler(streamHandler)

LOG.setLevel(logging.DEBUG)


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
    """ Just for testing. Return same JSON as received
    @return:
    """
    if request.method == 'POST':
        # LOG.debug("API MIRROR: {}".format(request.get_json(force=False, silent=False, cache=False)))
        return jsonify(request.get_json(force=False, silent=False, cache=False))


@app.route('/api/test', methods=['GET', 'POST'])
def api_test():
    """ Ping test
    @return:
    """
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

    flight = Controller.getFlightByNumber(flight_number)

    if json_request.has_key("data"):
        LOG.info("Telemetry data accepted")
        # Controller.checkTelemetryJsonData(json_request["data"])
        Controller.saveNewParameters(flight_number, json_request["data"])
        observer.update(flight.id)
        # WebController.refreshSite(flight_number)
        # SocialController.postStatuses(altitude,timestamp)

    return "OK", 201


@app.route('/api/flight/<int:flight_number>/event/<string:event>', methods=['POST'])
def api_events(flight_number, event):
    if request.method != 'POST':
        abort(405)

    # if not Controller.isValidEvent(event):
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
        Controller.saveNewEvent(flight_number, event, json_request["data"])
        observer.update(flight_id)
        # WebController.refreshSite(flight_number)

    return "OK", 201


@app.route('/api/chart/<int:flight_id>/<string:value>', methods=['POST', 'GET'])
def api_chart_getValues(flight_id, value):
    chartData = Controller.getChartData(flight_id, value)

    LOG.debug(chartData)

    import json_tricks
    data = json_tricks.dumps(chartData, primitives=True)
    return data


def checkDate(startDate):
    return True


@app.route('/api/flight', methods=['POST'])
def add_flight():
    if not request.method == 'POST':
        abort(405)

    if not request.json:
        abort(400)

    json_data = request.json
    LOG.debug(json_data)

    if not checkDate(json_data["startDate"]):
        # wring date
        abort(400)

    if Controller.flightExists(json_data["number"]):
        # Flight number exists
        abort(400)

    if Controller.saveNewFlight(json_data['number'], json_data['startDate']):
        flight = Controller.getFlightByNumber(json_data['number'])

        import time
        from flask import url_for
        data = {
            "id": flight.id,
            "number": flight.number,
            "hash": flight.hash,
            "start_date": time.mktime(flight.start_date.timetuple()),
            "urls": {
                "get": url_for('delete_flight', flight_id=flight.id),
                "delete": url_for('delete_flight', flight_id=flight.id)
            },
            "webUrls": {
                "detail": url_for('flight_detail', flight_id=flight.id)
            }
        }

        LOG.debug(data)
        return jsonify(data)


@app.route('/api/flight/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    flight = Controller.getFlightById(flight_id)
    if flight is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    import time
    from flask import url_for
    data = {
        "id": flight.id,
        "number": flight.number,
        "hash": flight.hash,
        "start_date": time.mktime(flight.start_date.timetuple()),
        "urls": {
            "add": url_for('add_flight'),
            "get": url_for('get_flight', flight_id=flight.id),
            "delete": url_for('delete_flight', flight_id=flight.id),
        },
        "webUrls": {
            "detail": url_for('flight_detail', flight_id=flight.id)
        }
    }

    LOG.debug(data)
    return jsonify(data)


@app.route('/api/flight/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = Controller.getFlightById(flight_id)

    if flight is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if Controller.deleteFlight(flight.id):
        return make_response(jsonify({'msg': 'Flight removed'}), 200)
    else:
        return make_response(jsonify({'error': 'Server error'}), 500)

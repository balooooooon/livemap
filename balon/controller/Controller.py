# http://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files

# Controller for Web, FB, API

from balon import app, LOG
from balon.models.Flight import Flight
from balon.service import BalloonService as service

import time
import datetime


# -------------------------
#      Webpage Dashboard
# -------------------------

def getBalloonLocation(flight_number):
    position = None

    # flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightLastPosition(flight_number)

    position = {
        'type': "current",
        'point': {
            'time': parameter.time_received,
            'lat': parameter.valuesDict["lat"].value,
            'lng': parameter.valuesDict["lng"].value
        }
    }

    LOG.debug("BalloonLocation: ", position)

    return position


def getBalloonStart(flight_number):
    position = None

    # flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightFirstPosition(flight_number)

    position = {
        'type': "start",
        'point': {
            'time': parameter.time_received,
            'lat': parameter.valuesDict["lat"].value,
            'lng': parameter.valuesDict["lng"].value
        }
    }

    LOG.debug("BalloonStart: ", position)

    return position


def getBalloonBurst(flight_number):
    location = None

    if app.config['NO_DB']:
        timestamp = 1477866660

        location = {
            'type': "burst",
            'point': {
                'time': timestamp,
                'lat': 48.687088,
                'lng': 19.667122
            }
        }

    return None


def getBalloonPath(flight_number):
    position = None

    # flight = service.getFlightByNumber(flight_number)
    parameters = service.getFlightPath(flight_number)

    path = {
        'type': "path",
        'data': {
            'points': []
        }
    }

    for p in parameters:
        LOG.debug(p)
        point = {
            'time': p.time_received,
            'lat': p.valuesDict["lat"].value,
            'lng': p.valuesDict["lng"].value
        }

        path["data"]["points"].append(point)

    LOG.debug("BalloonPath: ", path)

    return path


# -------------------------
#      API
# -------------------------

def authenticate(flight_number, auth_hash):
    # TODO
    if app.config["APP_AUTHENTICATE_FLIGHT"]:
        LOG.critical("Authenticating Not Implemented")
        return False
    else:
        return True


def saveNewParameters(flight_number, data):
    flight = service.getFlightByNumber(flight_number)
    # Get modified Flight object from DB

    time_received = int(time.time())
    # Get time of message receive

    service.saveParameterWithValues(flight, data, time_received)
    # Save new parameters

    return True


def getParametersAllByFlight(flight_id):
    flight = service.getFlightById(flight_id)
    parameters = service.getParametersWithValuesByFlight(flight.id)
    return parameters


def isValidEvent(event):
    """
    Check if event is valid
    :param event: String
    :return: True/False
    """
    # TODO
    return True


def saveEvent(param):
    # TODO
    return None


def saveNewFlight(number, datetime):
    LOG.info("Saving new Flight")

    datetime = parseHTMLDateTimeToDateTime(datetime)
    # Parse DateTime formated by HTML input tag to Python datetime object

    hash = service.computeHash(number)
    # Compute hash for Flight

    flight = Flight(int(number), hash, datetime)
    # Create new Flight object

    return service.saveNewFlight(flight)
    # Save new Flight object


def getFlightById(flight_id):
    flight = service.getFlightById(flight_id)
    return flight


def getFlightAll():
    flights = service.getFlightAll()
    return flights


def parseHTMLDateTimeToDateTime(date):
    """
    Thanks to:
        http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python

    :param date: HTML-formatted datetime
    :return: Python datetime object
    """
    from datetime import datetime as dt
    HTML_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
    timestamp = time.mktime(datetime.datetime.strptime(date, HTML_DATETIME_FORMAT).timetuple())
    return dt.fromtimestamp(timestamp)


def parseHTMLDateTimeToTimestamp(date):
    HTML_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
    timestamp = time.mktime(datetime.datetime.strptime(date, HTML_DATETIME_FORMAT).timetuple())
    return timestamp

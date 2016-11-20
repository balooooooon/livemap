# http://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files

# Controller for Web, FB, API

# import BalloonService
import time

import datetime

from balon import app, LOG
from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
from balon.service import BalloonService as service


def getBalloonLocation(flight_number):

    position = None

    flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightLastPosition(flight['id'])

    position = {
        'type': "current",
        'point': {
            'time': parameter.time_received,
            'lat': parameter.values["lat"].value,
            'lng': parameter.values["lng"].value
        }
    }

    LOG.debug("BalloonLocation: ",position)

    return position


def getBalloonStart(flight_number):
    position = None

    flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightFirstPosition(flight['id'])

    position = {
        'type': "start",
        'point': {
            'time': parameter.time_received,
            'lat': parameter.values["lat"].value,
            'lng': parameter.values["lng"].value
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

    flight = service.getFlightByNumber(flight_number)
    parameters = service.getFlightPath(flight['id'])

    path = {
        'type':"path",
        'data':{
            'points':[]
        }
    }

    for p in parameters:
        LOG.debug(p)
        point = {
            'time': p.time_received,
            'lat': p.values["lat"].value,
            'lng': p.values["lng"].value
        }

        path["data"]["points"].append(point)

    LOG.debug("BalloonPath: ", path)

    return path



def authenticate(flight_number, auth_hash):
    # TODO
    if app.config["APP_AUTHENTICATE_FLIGHT"]:
        LOG.critical("Authenticating Not Implemented")
        return False
    else:
        return True


def saveNewTelemetry(flight_number, data):
    LOG.debug(data)

    flight = service.getFlightByNumber(flight_number)

    time_received = int(time.time())

    service.saveParameterWithValues(flight, data, time_received)

    return None


def isValidEvent(event):
    return None


def saveEvent(param):
    return None

def saveNewFlight(number, datetime):
    LOG.info("Saving new Flight")

    datetime = parseHTMLDateTime(datetime)
    hash = service.computeHash(number)

    flight = Flight(int(number),hash,int(datetime))

    return service.saveNewFlight(flight)

def getFlightById(flight_id):
    flight = service.getFlightById(flight_id)
    return flight

def getFlightAll():
    flights = service.getFlightAll()
    return flights


def parseHTMLDateTime(date):
    HTML_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"

    timestamp = time.mktime(datetime.datetime.strptime(date, HTML_DATETIME_FORMAT).timetuple())
    # http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python

    return timestamp


def getParametersAllByFlight(flight_id):
    flight = service.getFlightById(flight_id)
    parameters = service.getParametersWithValuesByFlight(flight["id"])
    return parameters
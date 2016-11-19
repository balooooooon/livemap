# http://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files

# Controller for Web, FB, API

# import BalloonService
import time

import datetime

from balon import app
from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
from balon.service import BalloonService as service


def getBalloonLocation():
    location = None

    if app.config['NO_DB']:
        lat = 48.789562
        lng = 19.773012
        timestamp = 1477866660

        location = {
            'type': "current",
            'point': {
                'time': timestamp,
                'lat': lat,
                'lng': lng
            }
        }

    return location


def getBalloonStart():
    location = None

    if app.config['NO_DB']:
        timestamp = 1477866660

        location = {
            'type': "start",
            'point': {
                'time': timestamp,
                'lat': 48.649259,
                'lng': 19.358272
            }
        }

    return location


def getBalloonBurst():
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

    return location


def getBalloonPath():
    path = None

    if app.config['NO_DB']:
        timestamp = 1477866660

        path = {}
        path['type'] = 'path'
        path['data'] = {
            'points': [
                {'time': timestamp,
                 'lat': 48.649259,
                 'lng': 19.358272
                 },
                {'time': timestamp,
                 "lat": 48.755356,
                 "lng": 19.581007
                 },
                {'time': timestamp,
                 "lat": 48.687088,
                 "lng": 19.667122
                 },
                {'time': timestamp,
                 "lat": 48.789562,
                 "lng": 19.773012
                 }
            ]
        }

    return path


def authenticate(flight_number, auth_hash):
    # TODO
    if app.config["APP_AUTHENTICATE_FLIGHT"]:
        app.logger.critical("Authenticating Not Implemented")
        return False
    else:
        return True


def saveNewTelemetry(flight_number, data):
    app.logger.debug(data)
    print data

    flight = service.getFlightByNumber(flight_number)

    time_received = int(time.time())

    service.saveParameterWithValues(flight, data, time_received)

    return None


def isValidEvent(event):
    return None


def saveEvent(param):
    return None

def saveNewFlight(number, datetime):
    app.logger.info("Saving new Flight")

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
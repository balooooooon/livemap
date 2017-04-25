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
    """ Returns dictionary with current Balloon location, ready to send to webpage
    @param flight_number: Flight number
    @type flight_number: int
    @return: Dictionary with balloon location
    """
    position = None

    # flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightLastPosition(flight_number)

    if parameter is not None:
        position = {
            'type': "current",
            'point': {
                # 'time': parameter.time_received,
                'time': time.mktime(parameter.time_received.timetuple()),
                'lat': parameter.values["lat"].value,
                'lng': parameter.values["lng"].value
            }
        }

    LOG.debug("BalloonLocation: ", position)

    return position


def getBalloonStart(flight_number):
    """ Returns dictionary with starting Balloon location, ready to send to webpage
    @param flight_number: Flight number
    @type flight_number: int
    @return: Dictionary with balloon starting location
    """
    position = None

    # flight = service.getFlightByNumber(flight_number)
    parameter = service.getFlightFirstPosition(flight_number)

    if parameter is not None:
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
    """ Returns dictionary with Balloon location of burst, ready to send to webpage
    @param flight_number: Flight number
    @type flight_number: int
    @return: Dictionary with balloon burst location
    """
    position = None

    flight = service.getFlightByNumber(flight_number)
    events = service.getEventsByFlight(flight.id)

    for e in events:
        if e.type == "burst":
            # service.fillParametersDictionary(e)
            parameter = e.parameters["position"]
            position = {
                'type': "burst",
                'point': {
                    'time': parameter.time_received,
                    'lat': parameter.values["lat"].value,
                    'lng': parameter.values["lng"].value
                }
            }

    LOG.debug("BalloonBurst: ", position)

    return position


def getBalloonPath(flight_number):
    """ Returns dictionary with balloon flight path, ready to send to webpage
    @param flight_number: Flight number
    @type flight_number: int
    @return: Dictionary with balloon path
    """
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
            'lat': p.values["lat"].value,
            'lng': p.values["lng"].value
        }

        path["data"]["points"].append(point)

    LOG.debug("BalloonPath: ", path)

    return path


def getCurrentTelemetry(flight_id):
    parameterList = service.getLastTelemetry(flight_id)

    if parameterList is not None:
        data = {
            "type": "telemetry",
            "data": {
                "parameters": {
                    "altitude" : {
                        "name": "altitude",
                        "value": parameterList["position"].values["alt"].value,
                        "time": time.mktime(parameterList["position"].time_created.timetuple())
                    },
                    "temperature": {
                        "name": "temperature",
                        "value": parameterList["temperature"].values["out"].value,
                        "time": time.mktime(parameterList["position"].time_created.timetuple())
                    }
                }
            }
        }

        return data
    else:
        return None


# -------------------------
#      API
# -------------------------

def authenticate(flight_number, auth_hash):
    """ Authorize connection, when new flight data received
    @param flight_number:
    @param auth_hash:
    @return:
    """
    # TODO
    LOG.critical("Authenticating Not Implemented")
    if app.config["APP_AUTHENTICATE_FLIGHT"]:
        return False
    else:
        return True


def saveNewParameters(flight_number, data):
    # Get modified Flight object from DB
    flight = service.getFlightByNumber(flight_number)

    # Get time of message receive
    time_received = int(time.time())

    # Save new parameters
    service.saveParameterWithValues(flight, data, time_received)

    return True


def getParametersAllByFlight(flight_id):
    flight = service.getFlightById(flight_id)
    parameters = service.getParametersWithValuesByFlight(flight.id)
    return parameters


def getEventsAllByFlight(flight_id):
    flight = service.getFlightById(flight_id)
    events = service.getEventsByFlight(flight.id)
    return events

def isValidEvent(event,ev):
    """ Check if event is valid
    @param event: Event type
    @type event: string
    @return: True if event valid
    @rtype: bool
    """
    # TODO
    LOG.critical("isValidEvent NOT IMPLEMENTED")
    return True


def saveNewEvent(flight_number, event, data):
    LOG.info("Saving new Event")

    if not isValidEvent(data['event'], event):
        return False

    flight = service.getFlightByNumber(flight_number)

    time_received = int(time.time())

    return service.saveNewEvent(flight, data, time_received)


def saveNewFlight(number, datetime):
    LOG.info("Saving new Flight")

    # Parse DateTime formated by HTML input tag to Python datetime object
    datetime = parseHTMLDateTimeToDateTime(datetime)

    # Compute hash for Flight
    hash = service.computeHash(number)

    # Create new Flight object
    flight = Flight(number=int(number), hash=hash, start_date=datetime)

    # Save new Flight object
    return service.saveNewFlight(flight)

def deleteFlight(flight_id):
    res = service.deleteFlightById(flight_id)
    return res

def getFlightById(flight_id):
    flight = service.getFlightById(flight_id)
    return flight


def getFlightAll():
    flights = service.getFlightAll()
    return flights


def getFlightList():
    """ Returns list of all flights
    @return: array of flights
    """
    flightList = service.getFlightList()
    return flightList


def parseHTMLDateTimeToDateTime(date):
    """
    Thanks to:
        http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python

    @param date: HTML-formatted datetime
    @return: Python datetime object
    @rtype: datetime
    """
    from datetime import datetime as dt
    HTML_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
    timestamp = time.mktime(datetime.datetime.strptime(date, HTML_DATETIME_FORMAT).timetuple())
    return dt.fromtimestamp(timestamp)


def parseHTMLDateTimeToTimestamp(date):
    HTML_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
    timestamp = time.mktime(datetime.datetime.strptime(date, HTML_DATETIME_FORMAT).timetuple())
    return timestamp


def flightExists(flight_number):
    """ Checks if Flight with requested Flgiht Number exists in Database
    @param flight_number: Flight Number
    @rtype: boolean
    """
    flight = service.getFlightByNumber(flight_number)
    if flight is Flight:
        return True
    else:
        return False


def getFlightByNumber(flight_number):
    flight = service.getFlightByNumber(flight_number)
    if isinstance(flight, Flight):
        return flight
    else:
        return None


def getChartTypes(flight_id):
    charts = service.getChartTypes(flight_id) or None
    LOG.debug(charts)
    return charts


def getChartData(flight_id, value):
    chartData = service.getChartData(flight_id, value)
    return chartData

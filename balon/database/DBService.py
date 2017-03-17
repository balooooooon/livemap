import logging

from flask_sqlalchemy import get_debug_queries

from balon import db
from balon import app

from balon.models.Flight import Flight
from balon.models.Parameter import Parameter

LOG = logging.getLogger(app.config['LOGGING_LOGGER_DB'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setFormatter(formatter)
handler.setLevel(app.config['LOGGING_LEVEL'])
LOG.addHandler(handler)
LOG.setLevel(logging.DEBUG)


# -------------------------
#      Flight
# -------------------------

def getFlightByKey(key, value):
    q = {key: value}
    LOG.info("Query for flight with ",q)
    flight = Flight.query.filter_by(**q).first()
    return flight


def getFlightById(flight_id):
    LOG.info("Query for flight with id: %d",flight_id)
    return Flight.query.get(flight_id)


def getFlightAll():
    LOG.info("Query for all flights with ")
    flight =  Flight.query.all()
    return flight

def saveFlight(flight):
    db.session.add(flight)
    db.session.commit()
    return True


def updateFlight(flight):
    db.session.add(flight)
    db.session.commit()
    return True


def deleteFlight(flight):
    db.session.delete(flight)
    db.session.commit()
    return True


# -------------------------
#      Parameter
# -------------------------

def saveEvent(event):
    db.session.add(event)
    db.session.commit()
    return True


# -------------------------
#      Parameter
# -------------------------

def saveParameter(parameter):
    db.session.add(parameter)
    db.session.commit()
    return parameter.id


def getParametersByFlight(flight_id):
    flight = Flight.query.get(flight_id)
    parameters = flight.parameters
    return parameters


def getParametersByKeyByFlight(key, value, flight_id):
    q = {key: value, 'flight_id': flight_id}
    parameters = Parameter.query.filter_by(**q).order_by(Parameter.time_received).all()
    return parameters


def getParameterLastByFlight(key, value, flight_id):
    q = {key: value, 'flight_id': flight_id}
    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_created.desc()).first()
    return parameter


def getParameterFirstByFlight(key, value, flight_id):
    q = {key: value, 'flight_id': flight_id}
    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_created.asc()).first()
    return parameter


def getEventsByFlight(flight_id):
    flight = Flight.query.get(flight_id)
    events = flight.events
    return events
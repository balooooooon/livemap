from balon import db as newDB
from balon import app, LOG

from balon.models.Flight import Flight
from balon.models.Parameter import Parameter


# -------------------------
#      Flight
# -------------------------

def getFlightByKey(key, value):
    q = {key: value}
    flight = Flight.query.filter_by(**q).first()
    return flight


def getFlightById(flight_id):
    return Flight.query.get(flight_id)


def getFlightAll():
    return Flight.query.all()


def saveFlight(flight):
    newDB.session.add(flight)
    newDB.session.commit()
    return True


def updateFlight(flight):
    newDB.session.add(flight)
    newDB.session.commit()
    return True


def deleteFlight(flight):
    newDB.session.delete(flight)
    newDB.session.commit()
    return True


# -------------------------
#      Parameter
# -------------------------

def saveParameter(parameter):
    newDB.session.add(parameter)
    newDB.session.commit()
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
    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_received.desc()).first()
    return parameter


def getParameterFirstByFlight(key, value, flight_id):
    q = {key: value, 'flight_id': flight_id}
    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_received.asc()).first()
    return parameter


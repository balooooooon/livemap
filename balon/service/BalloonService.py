from balon import app, LOG, db
from balon.database import DBService as dao

from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
from balon.models.Value import Value

import hashlib
from datetime import datetime

def getValueUnit(type):
    # TODO
    return "m"


# -------------------------
#      Flight
# -------------------------

def getFlightById(flight_id):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_ID, flight_id)
    return flight


def getFlightByNumber(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    return flight


def saveNewFlight(flight):
    return dao.saveFlight(flight)


def getFlightAll():
    flights = dao.getFlightAll()
    return flights


def computeHash(number):
    m = hashlib.md5()
    m.update(number)
    return m.hexdigest()


# -------------------------
#      Parameters
# -------------------------

def saveParameterWithValues(flight, data, time_received):
    dt = float(data['timestamp'])
    parameters = data['parameters']

    for param in parameters:
        type = param['type']

        if param.has_key("timestamp"):
            time_created = datetime.fromtimestamp(float(param['timestamp']))
        else:
            time_created = datetime.fromtimestamp(dt)

        p = Parameter(type, datetime.fromtimestamp(time_received), time_created)

        inputValues = param['values']
        for key, val in inputValues.iteritems():
            unit = getValueUnit(type)
            p.values.append(Value(val, unit, key))

        flight.parameters.append(p)

    db.session.add(flight)
    db.session.commit()
    return True


def getParametersWithValuesByFlight(flight_id):
    # flight = dao.getFlightById(flight_id)
    parameters = dao.getParametersByFlight(flight_id)

    # Storing values in dicttionary for better retrieval
    # Possible to store in DB as PickleType
    for p in parameters:
        fillValuesDictionary(p)

    return parameters


# -------------------------
#      Object creation
# -------------------------

def getParameterObject(p, values):
    param = Parameter(p["flight_id"], p["type"], p["time_received"], p["time_created"])

    param.id = p[Parameter.ParameterEntry.KEY_ID]
    param.source = p["source"]
    param.valid = p["valid"]
    param.validated = p["validated"]

    param.values = {}
    for v in values:
        param.values[v["name"]] = getValueObject(v)

    return param


def getValueObject(v):
    value = Value(v["parameter_id"], v["value"], v["unit"], v["name"])
    return value


# -------------------------
#      For Dashboard
# -------------------------

def getFlightLastPosition(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    parameter = dao.getParameterLastByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight.id)
    LOG.debug(parameter)
    # param = dao.getParameterLastByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight_number)
    # values = dao.getValuesByKey(Value.ValueEntry.KEY_PARAMETER_ID, param["id"])
    fillValuesDictionary(parameter)
    # p = getParameterObject(param, values)
    return parameter


def getFlightFirstPosition(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    parameter = dao.getParameterFirstByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight.id)
    # param = dao.getParameterFirstByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight_id)
    # values = dao.getValuesByKey(Value.ValueEntry.KEY_PARAMETER_ID, param["id"])
    fillValuesDictionary(parameter)
    # p = getParameterObject(param, values)
    return parameter


def getFlightPath(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    parameters = dao.getParametersByKeyByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight.id)
    for p in parameters:
        fillValuesDictionary(p)

    return parameters

    params = []
    for p in dao.getParametersByKeyByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight_id):
        LOG.debug(p)
        values = dao.getValuesByKey(Value.ValueEntry.KEY_PARAMETER_ID, p["id"])
        params.append(getParameterObject(p, values))
    return params

def fillValuesDictionary(p):
    p.valuesDict = {}
    for v in p.values:
        p.valuesDict[v.name] = v
from balon import app, LOG
from balon.database import DBService as dao
from balon.models.Event import Event

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

def deleteFlightById(flight_id):
    return dao.deleteFlight(flight_id)


def getFlightAll():
    flights = dao.getFlightAll()
    return flights


def getFlightList():
    """
    Return list of all flights, their ID, number and start_date
    @return: array - array of all flights
    """
    flights = dao.getFlightAll()
    flightList = []
    for flight in flights:
        f = {"id": flight.id, "number": flight.number, "start_date": flight.start_date}
        flightList.append(f)
    return flightList


def computeHash(number):
    m = hashlib.md5()
    m.update(number)
    return m.hexdigest()


# -------------------------
#      Parameters
# -------------------------

def saveNewEvent(flight, data, time_received):
    dt = float(data['timestamp'])

    parameters = data['parameters']

    event = Event(flight_id=flight.id, type=data['event'], time_created=datetime.fromtimestamp(dt))
    event.id = dao.saveEvent(event)

    for param in parameters:
        type = param['type']

        if param.has_key("timestamp"):
            time_created = datetime.fromtimestamp(float(param['timestamp']))
        else:
            time_created = datetime.fromtimestamp(dt)

        p = Parameter(type=type, time_received=datetime.fromtimestamp(time_received), time_created=time_created, flight_id=flight.id)
        p.id = dao.saveParameter(p)
        dao.bindParameterToEvent(p.id, event.id)

        inputValues = param['values']
        for key, val in inputValues.iteritems():
            unit = getValueUnit(type)
            val = Value(value=val, unit=unit, name=key)
            p.values[key] = val
            dao.saveValue(val, p.id)

        flight.parameters.append(p)
        event.parameters[p.type] = p

    # dao.saveFlight(flight)

    return True


def saveParameterWithValues(flight, data, time_received):
    dt = float(data['timestamp'])
    parameters = data['parameters']

    for param in parameters:
        type = param['type']

        if param.has_key("timestamp"):
            time_created = datetime.fromtimestamp(float(param['timestamp']))
        else:
            time_created = datetime.fromtimestamp(dt)

        p = Parameter(flight_id=flight.id, type=type, time_received=datetime.fromtimestamp(time_received),
                      time_created=time_created)
        p.id = dao.saveParameter(p)

        inputValues = param['values']
        LOG.debug(inputValues)
        for key, val in inputValues.iteritems():
            unit = getValueUnit(type)
            val = Value(value=val, unit=unit, name=key)
            p.values[key] = val
            dao.saveValue(val, p.id)

        flight.parameters.append(p)

    # dao.saveFlight(flight)
    return True


def getParametersWithValuesByFlight(flight_id):
    # flight = dao.getFlightById(flight_id)
    parameters = dao.getParametersByFlight(flight_id)
    # Storing values in dicttionary for better retrieval
    # Possible to store in DB as PickleType
    # for p in parameters:
    #     fillValuesDictionary(p)
    return parameters


def getEventsByFlight(flight_id):
    events = dao.getEventsByFlight(flight_id)
    #for e in events:
    #    fillParametersDictionary(e)
    #    for p in e.parameters:
    #        fillValuesDictionary(p)

    return events


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
    #if parameter is not None:
    #    fillValuesDictionary(parameter)
    return parameter


def getFlightFirstPosition(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    parameter = dao.getParameterFirstByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight.id)
    #if parameter is not None:
    #    fillValuesDictionary(parameter)
    return parameter


def getFlightPath(flight_number):
    flight = dao.getFlightByKey(Flight.FlightEntry.KEY_NUMBER, flight_number)
    parameters = dao.getParametersByKeyByFlight(Parameter.ParameterEntry.KEY_TYPE, "position", flight.id)
    #for p in parameters:
    #    fillValuesDictionary(p)
    return parameters


def fillValuesDictionary(p):
    if p is None:
        raise TypeError("Parameter is Null")
    valuesDictTemp = {}
    for v in p.valuesDict:
        valuesDictTemp[v] = p.valuesDict[v].value

    return valuesDictTemp

def fillParametersDictionary(e):
    if e is None:
        raise TypeError("Parameter is Null")
    e.parametersDict = {}
    for p in e.parameters:
        fillValuesDictionary(p)
        e.parametersDict[p.type] = p


def getChartTypes(flight_id):
    parameterTypes = dao.getParameterTypes(flight_id)
    LOG.debug(parameterTypes)

    if parameterTypes is not None:
        for p in parameterTypes:
            LOG.debug(p)
            p["values"] = {}
            val = dao.getValueTypesByParameter(flight_id, p["type"])
            LOG.debug(val)
            p["values"] = val

        return parameterTypes
    else:
        return None


def getChartData(flight_id, value):
    """

    @param flight_id:
    @param value:
    @return: Data or None
    """
    data = dao.getParametersByKeyByFlight('value_1.name',value,flight_id) or None
    result = []
    for p in data:
        x = {}
        x["id"] = p.id
        x["time_received"] = p.time_received
        x["time_created"] = p.time_created
        x["val"] = p.values[value]
        result.append(x)
    return result



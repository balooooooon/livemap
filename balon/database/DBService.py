import logging
from contextlib import closing

import MySQLdb
#from flask_sqlalchemy import get_debug_queries

from balon import db
from balon import app

from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
# from balon.models.Parameter import Parameter
from balon.models.Value import Value
from balon.models.Event import Event

LOG = logging.getLogger(app.config['LOGGING_LOGGER_DB'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setFormatter(formatter)
handler.setLevel(app.config['LOGGING_LEVEL'])
LOG.addHandler(handler)
LOG.setLevel(logging.DEBUG)


if (app.config['LOGGING_CONSOLE_DB']):
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(app.config['LOGGING_LEVEL_CONSOLE'])
    streamHandler.setFormatter(formatter)
    # app.logger.addHandler(streamHandler)
    LOG.addHandler(streamHandler)
    
# -------------------------
#      Flight
# -------------------------

def getFlightByKey(key, value):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight " \
                "WHERE {} = {} LIMIT 1".format(key,value)

        LOG.debug(query)
        cur.execute(query)
        p = cur.fetchone()

    if p is None: return None
    return Flight(fromDB=p)


def getFlightById(flight_id):
        query = "SELECT * FROM flight " \
                "WHERE {} = {} LIMIT 1".format(Flight.flight_id_DB,flight_id)
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:

        LOG.debug(query)
        cur.execute(query)
        p = cur.fetchone()

    if p is None: return None
    return Flight(fromDB=p)


def getFlightAll():
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight"

        LOG.debug(query)
        cur.execute(query)

        flights = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            flights.append(Flight(fromDB=p))
            p = cur.fetchone()

    return flights


def saveFlight(flight):
    LOG.info("Query for flight save")
    LOG.debug(flight)

    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO flight ({},{},{}) " \
                "VALUES ('{}','{}','{}')".format(
            Flight.FlightEntry.KEY_NUMBER, Flight.FlightEntry.KEY_HASH, Flight.FlightEntry.KEY_START_DATE,
            flight.number, flight.hash, flight.start_date)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


def updateFlight(flight):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "UPDATE flight " \
                "SET {} = {}, {} = {}, {} = {} " \
                "WHERE {} = {}".format(Flight.FlightEntry.KEY_NUMBER, flight.number,
                                       Flight.FlightEntry.KEY_HASH, flight.hash,
                                       Flight.FlightEntry.KEY_START_DATE, flight.flight_start_date,
                                       Flight.FlightEntry.KEY_ID, flight.id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


def deleteFlight(flight):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "DELETE FROM flight " \
                "WHERE id = {}".format(flight.id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

    return True

# -------------------------
#      Event
# -------------------------

def saveEvent(event):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO event ({},{},{}) " \
                "VALUES ('{}','{}','{}')".format(
            Event.EventEntry.KEY_TYPE, Event.EventEntry.KEY_TIME_CREATED, Event.EventEntry.KEY_FLIGHT_ID,
            event.type, event.time_created, event.flight_id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


def getEventsByFlight(flight_id):
        with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
            query = "SELECT * FROM event " \
                    "WHERE {} = {}".format(Event.EventEntry.KEY_FLIGHT_ID, flight_id)

            LOG.debug(query)
            cur.execute(query)

            events = []
            p = cur.fetchone()
            while True:
                if p is None:
                    break
                event = Event(fromDB=p)

                events.append(event)
                p = cur.fetchone()

        return events
# -------------------------
#      Parameter
# -------------------------

def saveParameter(parameter):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO parameter ({},{},{},{})" \
                "VALUES ({},{},{},{})".format(
            Parameter.ParameterEntry.KEY_TYPE, Parameter.ParameterEntry.KEY_TIME_RECEIVED,
            Parameter.ParameterEntry.KEY_TIME_CREATED, Parameter.ParameterEntry.KEY_FLIGHT_ID,
            parameter.type, parameter.time_received, parameter.time_created, parameter.flight_id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


def getParametersByFlight(flight_id):
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE flight_id = {} ORDER BY parameter.id".format(flight_id)

        LOG.debug(query)
        cur.execute(query)

        parameters = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            param = Parameter(fromDB=p)
            pid = p["id"]

            while param.id == pid:
                val = Value(fromDB=p)
                param.valuesDict[val.name] = val
                p = cur.fetchone()
                if p is None:
                    break
                pid = p["id"]

            parameters.append(param)
            # p = cur.fetchone()

    return parameters

    flight = Flight.query.get(flight_id)
    parameters = flight.parameters
    return parameters


def getParametersByKeyByFlight(key, value, flight_id):
    # q = {key: value, 'flight_id': flight_id}
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {} ORDER BY parameter.id".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        parameters = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            param = Parameter(fromDB=p)
            pid = p["id"]

            while param.id == pid:
                val = Value(fromDB=p)
                param.valuesDict[val.name] = val
                p = cur.fetchone()
                if p is None:
                    break
                pid = p["id"]

            parameters.append(param)
            # p = cur.fetchone()

    return parameters

    # query = "SELECT * FROM flight WHERE id = 1"
    query = "SELECT * FROM parameter LEFT OUTER JOIN value AS value_1 ON value_1.parameter_id = parameter.id WHERE type = 'position' AND flight_id = 1"
    x = cur.execute(query)
    y = cur.fetchall()
    # LOG.debug("QUERY: ")
    LOG.debug(x)
    LOG.debug(y[0][1])
    # parameters = Parameter.query.filter_by(**q).order_by(Parameter.time_received).all()
    # parameters = Parameter.query.filter_by(**q).all()
    parameters = None
    return parameters


def getParameterLastByFlight(key, value, flight_id):
#    q = {key: value, 'flight_id': flight_id}

#-------------------------------------------------------
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {}" \
                "ORDER BY parameter.time_created DESC".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Parameter(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Value(fromDB=p)
            param.valuesDict[val.name] = val
            p = cur.fetchone()
            if p is None:
                break
            pid = p["id"]


    return param

#-------------------------------------------------------

    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_created.desc()).first()
    return parameter


def getParameterFirstByFlight(key, value, flight_id):
#    q = {key: value, 'flight_id': flight_id}

#-------------------------------------------------------
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {}" \
                "ORDER BY parameter.time_created ASC".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Parameter(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Value(fromDB=p)
            param.valuesDict[val.name] = val
            p = cur.fetchone()
            if p is None:
                break
            pid = p["id"]


    return param
#-------------------------------------------------------

    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_created.asc()).first()
    return parameter



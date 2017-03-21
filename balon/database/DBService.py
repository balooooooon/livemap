import logging
from contextlib import closing

import MySQLdb
#from flask_sqlalchemy import get_debug_queries

from balon import db
from balon import app
from balon import mysql

from balon.models.Flight import Flight
from balon.models.Param import Param
#from balon.models.Parameter import Parameter
from balon.models.Val import Val
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
    q = {key: value}
    LOG.info("Query for flight with ", q)

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight " \
                "WHERE {} = {} ".format(key,value)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        flight = Flight(fromDB=p)

    return flight


def getFlightById(flight_id):
    LOG.info("Query for flight with id: %d",flight_id)

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight " \
                "WHERE {} = {} ".format(Flight.flight_id_DB,value)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        
        flight = Flight(fromDB=p)

    return flight


def getFlightAll():
    LOG.info("Query for all flights with")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight"

        LOG.debug(query)
        cur.execute(query)

        flights = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            flight = Flight(fromDB=p)

            flights.append(flight)
            p = cur.fetchone()

    return flights


def saveFlight(flight):
    LOG.info("Query for flight save")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO flight " \
                "VALUES ({},{},{})".format(flight.number,flight.hash,flight.start_date)

        LOG.debug(query)

        try:
            cur.execute(query)
            mysql.commit()
        except:     
            mysql.rollback()
            return False

    return True


def updateFlight(flight):

    LOG.info("Query for flight update")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "UPDATE flight " \
                "SET {} = {}, {} = {}, {} = {}" \
                "WHERE {} = {}".format(Flight.flight_number_DB,flight.number,Flight.flight_hash_DB,flight.hash,Flight.flight_start_date_DB,flight.flight_start_date,Flight.flight_id_DB,flight.id)

        LOG.debug(query)

        try:
            cur.execute(query)
            mysql.commit()
        except:     
            mysql.rollback()
            return False

    return True

    db.session.add(flight)
    db.session.commit()
    return True


def deleteFlight(flight):

    LOG.info("Query for flight delete")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "DELETE FROM flight " \
                "WHERE id = {}".format(flight.id)

        LOG.debug(query)

        try:
            cur.execute(query)
            mysql.commit()
        except:     
            mysql.rollback()
            return False

    return True

# -------------------------
#      Event
# -------------------------

def saveEvent(event):
    db.session.add(event)
    db.session.commit()
    return True


# -------------------------
#      Parameter
# -------------------------

def saveParameter(parameter):

    LOG.info("Query for parameter save")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO parameter ({},{},{},{})" \
                "VALUES ({},{},{},{})".format(Param.type_DB,Param.time_received_DB,Param.time_created_DB,Param.flight_id_DB,parameter.type,parameter.time_received,parameter.time_created,parameter.flight_id)

        LOG.debug(query)

        try:
            cur.execute(query)
            mysql.commit()
        except:     
            mysql.rollback()
            return False

    return True

    db.session.add(parameter)
    db.session.commit()
    return cursor.lastrowid


def getParametersByFlight(flight_id):
    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE flight_id = {} ORDER BY parameter.id".format(flight_id)

        LOG.debug(query)
        cur.execute(query)

        parameters = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            param = Param(fromDB=p)
            pid = p["id"]

            while param.id == pid:
                val = Val(p["value"], p["unit"], p["name"], p["value_1.id"])
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
    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {} ORDER BY parameter.id".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        parameters = []
        p = cur.fetchone()
        while True:
            if p is None:
                break
            param = Param(fromDB=p)
            pid = p["id"]

            while param.id == pid:
                val = Val(p["value"], p["unit"], p["name"], p["value_1.id"])
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
    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {}" \
                "ORDER BY parameter.time_created DESC".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Param(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Val(p["value"], p["unit"], p["name"], p["value_1.id"])
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
    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {}" \
                "ORDER BY parameter.time_created ASC".format(key,value,flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Param(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Val(p["value"], p["unit"], p["name"], p["value_1.id"])
            param.valuesDict[val.name] = val
            p = cur.fetchone()
            if p is None:
                break
            pid = p["id"]


    return param
#-------------------------------------------------------

    parameter = Parameter.query.filter_by(**q).order_by(Parameter.time_created.asc()).first()
    return parameter


def getEventsByFlight(flight_id):

    LOG.info("Query for all events for flight")

    with closing(mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM event " \
                "WHERE {} = {}".format(Event.event_id_DB,flight_id)

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


#------------------------------------
    flight = Flight.query.get(flight_id)
    events = flight.events
    return events
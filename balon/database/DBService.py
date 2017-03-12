import logging
from contextlib import closing

import MySQLdb
from flask_sqlalchemy import get_debug_queries

from balon import db
from balon import app
from balon import mysql

from balon.models.Flight import Flight
from balon.models.Param import Param
from balon.models.Parameter import Parameter
from balon.models.Val import Val

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
    LOG.info("Query for flight with ",q)
    flight = Flight.query.filter_by(**q).first()
    return flight


def getFlightById(flight_id):
    LOG.info("Query for flight with id: %d",flight_id)
    return Flight.query.get(flight_id)


def getFlightAll():
    LOG.info("Query for all flights with ")
    flight =  Flight.query.all()
    LOG.info(get_debug_queries()[0])
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
import logging
from contextlib import closing

import MySQLdb
from flask_sqlalchemy import get_debug_queries

from balon import app
from balon.database import DBConnector

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


def mysql_error_handler_decorator(func):
    """ Database query decorator.
    Checks for errors from MySQL Database
    @param func: DBService function
    @return: DBService function return value
    """
    def func_wrapper(*args, **kwargs):
        LOG.debug("mysql_error_handler_decorator")
        try:
            # Run DBService function
            res = func(*args, **kwargs)
        except MySQLdb.OperationalError as e:
            if e[0] == 2006:
                # If MySQL closed application connection after defined timeout, try reconnect
                LOG.error("MySQL database connection timeout.")
                DBConnector.connect_db(app)
            res = func(*args, **kwargs)
        return res
    return func_wrapper


# -------------------------
#      Flight
# -------------------------

@mysql_error_handler_decorator
def getFlightByKey(key, value):
    """ Returns Flight by specified key and value
    @param key: Flight parameter defined in Flight.FlightEntry
    @type key: Flight.FlightEntry.*
    @param value: Specified value of key
    @return: Flight object
    @rtype: Flight or None
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight " \
                "WHERE {} = {} LIMIT 1".format(key, value)

        LOG.debug(query)
        cur.execute(query)
        p = cur.fetchone()

    if p is None: return None
    return Flight(fromDB=p)


@mysql_error_handler_decorator
def getFlightById(flight_id):
    """ Returns Flight by specified ID
    @param flight_id: Flight ID
    @type flight_id: int
    @return: Flight object
    @rtype: Flight or None
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM flight WHERE id = {} LIMIT 1".format(flight_id)

        LOG.debug(query)
        cur.execute(query)
        p = cur.fetchone()

    if p is None: return None
    return Flight(fromDB=p)


@mysql_error_handler_decorator
def getFlightAll():
    """ Return all flights in database
    @return: array of Flights
    @rtype: Flight[]
    """
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


@mysql_error_handler_decorator
def saveFlight(flight):
    """ Save new Flight to database
    @param flight: New Flight object
    @type flight: Flight
    @return: Flight ID if Flight successfully saved to DB
    @rtype: int or False
    """
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


@mysql_error_handler_decorator
def updateFlight(flight):
    """ Update existing Flight in database
    @param flight: Flight object
    @type flight: Flight
    @return: Flight ID if Flight successfully updated
    @rtype: int or False
    """
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


@mysql_error_handler_decorator
def deleteFlight(flight_id):
    """ Delete Flight from database
    @param flight_id: Flight ID
    @type flight_id: int
    @return: True if Flight successfully deleted
    @rtype: bool
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "DELETE FROM flight " \
                "WHERE id = {}".format(flight_id)

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

@mysql_error_handler_decorator
def saveEvent(event):
    """ Save new Event to database
    @param event: New Event object
    @type event: Event
    @return: Event ID if event successfully saved to DB
    @rtype: int or False
    """
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


@mysql_error_handler_decorator
def bindParameterToEvent(param_id, event_id):
    """ Binds Parameter to specified Event in param_event Table
    @param param_id: Parameter ID
    @type param_id: int
    @param event_id: Event ID
    @type event_id: int
    @return: Something?
    @rtype: itn or False
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO param_event (parameter_id,event_id) " \
                "VALUES ('{}','{}')".format(param_id, event_id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


@mysql_error_handler_decorator
def getEventsByFlight(flight_id):
    """ Returns events for flight with specified ID
    @param flight_id: Flight ID
    @type flight_id: int
    @return: Array of Events
    @rtype: Event[]
    """
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

    for e in events:
        parameters = getParametersByEvent(e.id)
        e.parameters = {}
        for p in parameters:
            e.parameters[p.type] = p
        LOG.debug(e.parameters)

    return events


# -------------------------
#      Parameter
# -------------------------

@mysql_error_handler_decorator
def saveParameter(parameter):
    """ Save new Parameter to database
    @param parameter: New Parameter object
    @type parameter: Parameter
    @return: Parameter ID if parameter successfully saved to DB.
    @rtype: int or False
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO parameter ({},{},{},{})" \
                "VALUES ('{}','{}','{}','{}')".format(
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


@mysql_error_handler_decorator
def getParametersByFlight(flight_id):
    """ Returns parameters for flight with specified ID
        @param flight_id: Flight ID
        @type flight_id: int
        @return: Array of Parameters
        @rtype: Parameter[]
        """
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
                param.values[val.name] = val
                p = cur.fetchone()
                if p is None:
                    break
                pid = p["id"]

            parameters.append(param)
            # p = cur.fetchone()

    return parameters


@mysql_error_handler_decorator
def getParametersByEvent(event_id):
    """ Returns parameters for event with specified ID
        @param event_id: Event ID
        @type event_id: int
        @return: Array of Parameters
        @rtype: Parameter[]
        """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE parameter.id IN ( SELECT parameter_id FROM param_event WHERE event_id = {} )".format(event_id)

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
                param.values[val.name] = val
                p = cur.fetchone()
                if p is None:
                    break
                pid = p["id"]

            parameters.append(param)
            # p = cur.fetchone()

    return parameters


@mysql_error_handler_decorator
def getParametersByKeyByFlight(key, value, flight_id, order="ASC"):
    """ Returns parameters by specified key and value for flight specified by ID.
    @param key: Parameter attribute specified in Parameter.ParameterEntry
    @type key: Parameter.ParameterEntry.*
    @param value: Value of specified attribute
    @param flight_id: Flight ID
    @type flight_id: int
    @param order: Ordered by ID ascending or descending
    @type order: "ASC" or "DESC"
    @return: Array of Parameters
    @rtype: Parameter[]
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {} ORDER BY parameter.id".format(key, value, flight_id)

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
                param.values[val.name] = val
                p = cur.fetchone()
                if p is None:
                    break
                pid = p["id"]

            parameters.append(param)

    return parameters


@mysql_error_handler_decorator
def getParameterLastByFlight(key, value, flight_id):
    """ Returns last Parameter by specified key and value for flight specified by ID.
    @param key: Parameter attribute specified in Parameter.ParameterEntry
    @type key: Parameter.ParameterEntry.*
    @param value: Value of specified attribute
    @param flight_id: Flight ID
    @type flight_id: int
    @return: Parameter object
    @rtype: Parameter or None
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {} " \
                "ORDER BY parameter.time_created DESC".format(key, value, flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Parameter(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Value(fromDB=p)
            param.values[val.name] = val
            p = cur.fetchone()
            if p is None:
                break
            pid = p["id"]

    return param


@mysql_error_handler_decorator
def getParameterFirstByFlight(key, value, flight_id):
    """ Returns first Parameter by specified key and value for flight specified by ID.
    @param key: Parameter attribute specified in Parameter.ParameterEntry
    @type key: Parameter.ParameterEntry.*
    @param value: Value of specified attribute
    @param flight_id: Flight ID
    @type flight_id: int
    @return: Parameter object
    @rtype: Parameter or None
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "SELECT * FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
                "WHERE {} = '{}' AND flight_id = {} " \
                "ORDER BY parameter.time_created ASC".format(key, value, flight_id)

        LOG.debug(query)
        cur.execute(query)

        p = cur.fetchone()
        if p is None:
            return None
        param = Parameter(fromDB=p)
        pid = p["id"]

        while param.id == pid:
            val = Value(fromDB=p)
            param.values[val.name] = val
            p = cur.fetchone()
            if p is None:
                break
            pid = p["id"]

    return param


# -------------------------
#      Parameter
# -------------------------

@mysql_error_handler_decorator
def saveValue(value, parameter_id):
    """ Save new Value to database
    @param value: New Value object
    @type value: Value
    @param parameter_id: Parameter ID
    @type parameter_id: int
    @return: Value ID id Value successfully saved to DB
    @rtype: Value or False
    """
    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        query = "INSERT INTO value ({},{},{},{}) " \
                "VALUES ('{}','{}','{}','{}')".format(
            Value.ValueEntry.KEY_NAME, Value.ValueEntry.KEY_VALUE, Value.ValueEntry.KEY_UNIT,
            Value.ValueEntry.KEY_PARAMETER_ID,
            value.name, value.value, value.unit, parameter_id)

        LOG.debug(query)

        try:
            cur.execute(query)
            app.mysql.commit()
        except MySQLdb.Error, e:
            LOG.error(e)
            app.mysql.rollback()
            return False

        return cur.lastrowid


@mysql_error_handler_decorator
def getParameterTypes(flight_id):
    """ Returns all types of Parameters saved in databse for Flight with specified ID.
    @param flight_id: Flight ID
    @type flight_id: int
    @return: Array of Parameter types
    @rtype: dict[]{'type'}or None
    """
    query = "SELECT type FROM parameter WHERE flight_id = '{}' GROUP BY type".format(flight_id)

    types = None

    with closing(app.mysql.cursor(MySQLdb.cursors.SSDictCursor)) as cur:
        LOG.debug(query)
        cur.execute(query)
        types = cur.fetchall()

    if len(types) == 0:
        return None

    return types


@mysql_error_handler_decorator
def getValueTypesByParameter(flight_id, type):
    """ Returns all types of values for specified parameter saved in database for Flight with specified ID.
    @param flight_id: Flight ID
    @type flight_id: int
    @param type: Parameter type
    @type type: string
    @return: Array of Value types
    @rtype: dict[]{'name'} or None
    """
    query = "SELECT name FROM parameter LEFT JOIN value AS value_1 ON value_1.parameter_id = parameter.id " \
            "WHERE flight_id = {} AND type = '{}' GROUP BY value_1.name".format(flight_id, type)

    types = None

    with closing(app.mysql.cursor(MySQLdb.cursors.SSCursor)) as cur:
        LOG.debug(query)
        cur.execute(query)
        types = cur.fetchall()

    if len(types) == 0:
        return None

    return types

import sqlite3

from balon import app, LOG
import DBConnector as dbConnector
from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
from balon.models.Value import Value


# ----- FLIGHT -----

def getFlightByKey(key, value):
    db = dbConnector.get_db()
    cur = db.execute(
        "SELECT id, number, hash, start_date FROM '{tn}' WHERE {k}={v}". \
            format(tn=Flight.FlightEntry.TABLE_NAME, k=key, v=value))
    flight = cur.fetchone()
    return flight


def getFlightAll():
    db = dbConnector.get_db()
    cur = db.execute("SELECT id, number, hash, start_date FROM '{tn}'".\
                     format(tn=Flight.FlightEntry.TABLE_NAME))
    flights = cur.fetchall()
    return flights


def saveFlight(flight):
    if not isinstance(flight, Flight):
        LOG.error("Object is not class Flight")
        # TODO Exception
        return False

    db = dbConnector.get_db()
    db.execute("INSERT INTO 'flights' (number,hash,start_date) VALUES ( ?, ?, ? )",
               (flight.number, flight.hash, flight.start_date))
    db.commit()

    return True


def updateFlight(flight):
    if not isinstance(flight, Flight):
        LOG.error("Object is not class Flight")
        # TODO Exception
        return False

    db = dbConnector.get_db()
    db.execute("INSERT INTO 'flights' (number,hash,start_date) VALUES ( ?, ?, ? ) WHERE 'id'=?",
               (flight.number, flight.hash, flight.start_date, flight.id))
    db.commit()


# ----- PARAMETER -----


def saveParameter(parameter):
    if not isinstance(parameter, Parameter):
        return False

    db = dbConnector.get_db()
    cur = db.execute("INSERT INTO parameters (flight_id,type,time_received,time_created) VALUES (?,?,?,?)",
                     (parameter.flight_id, parameter.type, parameter.time_received, parameter.time_created))
    db.commit()
    if not cur.lastrowid > 0:
        # TODO Exception
        return False

    return cur.lastrowid


def getParametersByFlight(flight_id):
    return getParametersByKey(Parameter.ParameterEntry.KEY_FLIGHT_ID, flight_id)


def getParametersByKey(key, value):
    db = dbConnector.get_db()
    cur = db.execute(
        "SELECT * FROM '{tn}' WHERE {k}={v}".format(tn=Parameter.ParameterEntry.TABLE_NAME, k=key, v=value))
    parameters = cur.fetchall()
    return parameters


# ----- VALUE -----


def saveValue(value):
    if not isinstance(value,Value):
        return False

    db = dbConnector.get_db()
    cur = db.execute("INSERT INTO 'values' (parameter_id,name,value,unit) VALUES (?,?,?,?)",
                     (value.parameter_id, value.name, value.value, value.unit))
    db.commit()
    return cur.lastrowid


def saveValues(values):
    for val in values:
        if not isinstance(val, Value):
            # TODO Exception
            return False
    db = dbConnector.get_db()

    try:
        for val in values:
            cur = db.execute("INSERT INTO 'values' (parameter_id,name,value,unit) VALUES (?,?,?,?)",
                             (val.parameter_id, val.name, val.value, val.unit))
        db.commit()

    except db.Error, e:
        LOG.error("DB Error: %s", e.args[0])
        return False

    return True


def getValuesByKey(key, value):
    db = dbConnector.get_db()
    cur = db.execute("SELECT * FROM '{tn}' WHERE {k}={v}".format(tn=Value.ValueEntry.TABLE_NAME, k=key, v=value))
    values = cur.fetchall()
    return values

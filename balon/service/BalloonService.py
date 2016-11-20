# http://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
import hashlib

from balon.database import DBService as dao
from balon import app, LOG
from balon.models.Flight import Flight
from balon.models.Parameter import Parameter
from balon.models.Value import Value


class BalloonService():
    app = None

    def getBalloonLocation(self, ):
        if self.app.config['NO_DB']:
            lat = 48.789562
            lng = 19.773012
            timestamp = 1477866660

            location = {
                'type': "current",
                'point': {
                    'time': timestamp,
                    'lat': lat,
                    'lng': lng
                }
            }

        return location

    def getBalloonStart(self):
        if self.app.config['NO_DB']:
            timestamp = 1477866660

            location = {
                'type': "start",
                'point': {
                    'time': timestamp,
                    'lat': 48.649259,
                    'lng': 19.358272
                }
            }

        return location

    def getBalloonBurst(self):
        if self.app.config['NO_DB']:
            timestamp = 1477866660

            location = {
                'type': "burst",
                'point': {
                    'time': timestamp,
                    'lat': 48.687088,
                    'lng': 19.667122
                }
            }

        return location

    def getBalloonPath(self):
        if self.app.config['NO_DB']:
            timestamp = 1477866660

            path = {}
            path['type'] = 'path'
            path['data'] = {
                'points': [
                    {'time': timestamp,
                     'lat': 48.649259,
                     'lng': 19.358272
                     },
                    {'time': timestamp,
                     "lat": 48.755356,
                     "lng": 19.581007
                     },
                    {'time': timestamp,
                     "lat": 48.687088,
                     "lng": 19.667122
                     },
                    {'time': timestamp,
                     "lat": 48.789562,
                     "lng": 19.773012
                     }
                ]
            }

        return path


def getValueUnit(type):
    #TODO
    return "m"


def saveParameterWithValues(flight, data, time_received):
    LOG.debug("saving paramter")

    datetime = data['timestamp']

    parameters = data['parameters']

    for param in parameters:
        type = param['type']
        time_created = None

        if param.has_key("timestamp"):
            time_created = param['timestamp']
        else:
            time_created = datetime

        p = Parameter(flight['id'],type,time_received,time_created)
        p.id = dao.saveParameter(p)

        values = []
        values_dict = param['values']
        for val in values_dict:
            unit = getValueUnit(type)
            name,value = val.items()[0]
            values.append(Value(p.id,value,unit,name))

        dao.saveValues(values)

    return None


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
    hash = m.hexdigest()

    LOG.debug("Calculated hash for number %d: %s", number, hash)
    return hash


def getParameterObject(p, values):
    param = Parameter(p["flight_id"],p["type"],p["time_received"],p["time_created"])

    param.id = p[Parameter.ParameterEntry.KEY_ID]
    param.source = p["source"]
    param.valid = p["valid"]
    param.validated = p["validated"]

    param.values = values

    return param;



def getParametersWithValuesByFlight(flight_id):

    params = []
    for p in dao.getParametersByFlight(flight_id):
        values = dao.getValuesByKey(Value.ValueEntry.KEY_PARAMETER_ID,p["id"])
        params.append(getParameterObject(p,values))

    return params
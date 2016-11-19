

class Parameter(object):

    class ParameterEntry():
        TABLE_NAME = "parameters"
        KEY_ID = "id"
        KEY_FLIGHT_ID = "flight_id"
        KEY_TYPE = "type"
        KEY_SOURCE = "source"
        KEY_VALID = "valid"
        KEY_VALIDATED = "validated"
        KEY_TIME_RECEIVED = "time_received"
        KEY_TIME_CREATED = "time_created"


    def __init__(self, flight_id, type, time_received, time_created):
        self.id = None
        self.flight_id = flight_id

        self.type = type
        self.time_received = time_received
        self.time_created = time_created

        self.source = None
        self.valid = None
        self.validated = None

        self.values = None

    def __repr__(self):
        return '<Parameter [%d] [F:%d] %r >' % (self.id, self.flight_id, self.type)

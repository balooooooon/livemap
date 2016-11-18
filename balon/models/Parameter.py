

class Parameter(object):
    def __init__(self, flight_id, type, time_received, time_created):
        self.id = None
        self.flight_id = flight_id

        self.type = type
        self.time_received = time_received
        self.time_created = time_created

        self.type = None
        self.source = None
        self.valid = None
        self.validated = None

    def __repr__(self):
        return '<Parameter [%d] [F:%d] %r >' % (self.id, self.flight_id, self.type)

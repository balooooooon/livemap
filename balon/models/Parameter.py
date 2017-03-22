from flask import json


class Parameter(object):

    class ParameterEntry():
        TABLE_NAME = "parameter"

        KEY_ID = "id"
        KEY_FLIGHT_ID = "flight_id"
        KEY_TYPE = "type"
        KEY_SOURCE = "source"
        KEY_VALID = "valid"
        KEY_VALIDATED = "validated"
        KEY_TIME_RECEIVED = "time_received"
        KEY_TIME_CREATED = "time_created"

    def __init__(self,*args,**kwargs):
        if kwargs.has_key("fromDB"):
            fromDB = kwargs["fromDB"]
            if fromDB is None: raise ValueError()

            self.id = fromDB["id"]
            self.flight_id = fromDB["flight_id"]
            self.type = fromDB["type"]
            self.source = fromDB["source"]
            self.valid = fromDB["valid"]
            self.validated = fromDB["validated"]
            self.time_received = fromDB["time_received"]
            self.time_created = fromDB["time_created"]
            self.values = {}
        else:
            self.id = kwargs.get("id",None)
            self.flight_id = kwargs.get("flight_id",None)
            self.type = kwargs.get("type",None)
            self.source = kwargs.get("source",None)
            self.valid = kwargs.get("valid",None)
            self.validated = kwargs.get("validated",None)
            self.time_received = kwargs.get("time_received",None)
            self.time_created = kwargs.get("time_created",None)
            self.values = kwargs.get("values",{})

    def __repr__(self):
        return '<Parameter [%d] [F:%d] %r >' % (self.id, self.flight_id, self.type)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
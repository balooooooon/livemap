from flask import json


class Param(object):

    flight_start_date_DB = "start_date"

    param_type_DB = "type"
    param_time_received_DB = "time_received"
    param_time_created_DB = "time_created"
    param_flight_id_DB = "flight_id"
    param_source_DB = "source"
    param_valid_DB = "valid"
    param_validated_DB = "validated"

    def __init__(self,*args,**kwargs):
        if kwargs.has_key("fromDB"):
            fromDB = kwargs["fromDB"]
            self.id = fromDB["id"]
            self.flight_id = fromDB["flight_id"]
            self.type = fromDB["type"]
            self.source = fromDB["source"]
            self.valid = fromDB["valid"]
            self.validated = fromDB["validated"]
            self.time_received = fromDB["time_received"]
            self.time_created = fromDB["time_created"]
            self.valuesDict = {}
        else:
            self.id = None
            self.flight_id = None
            self.type = args[0]
            self.source = None
            self.valid = None
            self.validated = None
            self.time_received = args[1]
            self.time_created = args[2]
            self.valuesDict = {}

    def __repr__(self):
        return '<Parameter [%d] [F:%d] %r >' % (self.id, self.flight_id, self.type)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
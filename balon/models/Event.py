from flask import json

class Event(object):

    event_id_DB = "id"
    event_type_DB = "type"
    event_flight_id_DB = "flight_id"
    event_time_created_DB = "time_created"

    def __init__(self,*args,**kwargs):
        if kwargs.has_key("fromDB"):
            fromDB = kwargs["fromDB"]
            if fromDB is None: raise ValueError()

            self.id = fromDB["id"]
            self.type = fromDB["type"]
            self.flight_id = fromDB["flight_id"]
            self.time_created = fromDB["time_created"]
        else:
            self.id = None
            self.type = kwargs["type"]
            self.flight_id = kwargs["flight_id"]
            self.time_created = kwargs["time_created"]

    def __str__(self):
        return '<Event [%d] [%s] %d / Flight id - %s  >' % (self.id, str(self.time_created), self.type, self.flight_id)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)

from flask import json

class Event(object):

    class EventEntry:
        TABLE_NAME = "event"

        KEY_ID = "id"
        KEY_TYPE = "type"
        KEY_TIME_CREATED = "time_created"
        KEY_FLIGHT_ID = "flight_id"

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

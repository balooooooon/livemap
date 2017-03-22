from flask import json

class Flight(object):

    flight_number_DB = "number"
    flight_id_DB = "id"
    flight_hash_DB = "hash"
    flight_start_date_DB = "start_date"

    def __init__(self,*args,**kwargs):
        if kwargs.has_key("fromDB"):
            fromDB = kwargs["fromDB"]
            if fromDB is None: raise ValueError()

            self.id = fromDB["id"]
            self.number = fromDB["number"]
            self.hash = fromDB["hash"]
            self.start_date = fromDB["start_date"]
        else:
            self.id = None
            self.number = kwargs["number"]
            self.hash = kwargs["hash"]
            self.start_date = kwargs["start_date"]

    def __str__(self):
        return '<Flight [%d] [%s] %d / %s  >' % (self.id, str(self.start_date), self.number, self.hash)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)

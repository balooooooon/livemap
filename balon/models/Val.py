from flask import json


class Val(object):
    def __init__(self, value, unit, name, id=None):
        self.value = value
        self.unit = unit
        self.name = name
        self.id = id

    def __repr__(self):
        return '<Value [%d] %r = %f>' % (self.id, self.name, self.value)

    def __str__(self):
        return '<Value [%d] %r = %f>' % (self.id, self.name, self.value)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
from flask import json


class Value(object):
    class ValueEntry:
        TABLE_NAME = "value"

        KEY_ID = "id"
        KEY_VALUE = "value"
        KEY_UNIT = "unit"
        KEY_NAME = "name"
        KEY_PARAMETER_ID = "parameter_id"

    def __init__(self,*args,**kwargs):
        if kwargs.has_key("fromDB"):
            fromDB = kwargs["fromDB"]
            if fromDB is None: raise ValueError()

            self.id = fromDB["value_1.id"]
            self.value = fromDB["value"]
            self.unit = fromDB["unit"]
            self.name = fromDB["name"]
        else:
            self.id = kwargs.get("id",None)
            self.value = kwargs.get("value",None)
            self.unit = kwargs.get("unit",None)
            self.name = kwargs.get("name",None)

    def __repr__(self):
        return '<Value [%d] %r = %f>' % (self.id, self.name, self.value)

    def __str__(self):
        return '<Value [%d] %r = %f>' % (self.id, self.name, self.value)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
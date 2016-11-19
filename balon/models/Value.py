
class Value():

    class ValueEntry():
        TABLE_NAME = "values"

        KEY_ID = "id"
        KEY_VALUE = "value"
        KEY_UNIT = "unit"
        KEY_NAME = "name"
        KEY_PARAMETER_ID = "parameter_id"

    def __init__(self, parameter_id, value, unit, name):
        self.id = 0
        self.value = value
        self.name = name
        self.parameter_id = parameter_id
        self.unit = unit

    def __repr__(self):
        return '<Value [%d] [P:%d] %r = %f>' % (self.id, self.parameter_id, self.name, self.value)
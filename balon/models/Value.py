
class Value():

    def __init__(self, parameter_id, value, unit, name):
        self.id = None
        self.value = value
        self.name = name
        self.parameter_id = parameter_id
        self.unit = unit

    def __repr__(self):
        return '<Value [%d] [P:%d] %r = %f>' % (self.id, self.parameter_id, self.name, self.value)
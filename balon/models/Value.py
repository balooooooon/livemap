from balon import db

class Value(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.Float)
    unit = db.Column(db.String(5))
    parameter_id = db.Column(db.Integer,db.ForeignKey('parameter.id'))

    class ValueEntry:
        TABLE_NAME = "value"

        KEY_ID = "id"
        KEY_VALUE = "value"
        KEY_UNIT = "unit"
        KEY_NAME = "name"
        KEY_PARAMETER_ID = "parameter_id"

    def __init__(self, value, unit, name):
        self.value = value
        self.name = name
        self.unit = unit

    def __repr__(self):
        return '<Value [%d] [P:%d] %r = %f>' % (self.id, self.parameter_id, self.name, self.value)

    def __str__(self):
        return '<Value [%d] [P:%d] %r = %f>' % (self.id, self.parameter_id, self.name, self.value)
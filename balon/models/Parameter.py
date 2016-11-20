from balon import db


class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(20))
    source = db.Column(db.String(20))

    valid = db.Column(db.Boolean)
    validated = db.Column(db.Boolean)

    time_received = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)

    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    values = db.relationship('Value', backref="parameter", lazy='dynamic')

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

    def __init__(self, type, time_received, time_created):
        self.type = type
        self.time_received = time_received
        self.time_created = time_created
        self.valuesDict = None

    def __repr__(self):
        return '<Parameter [%d] [F:%d] %r >' % (self.id, self.flight_id, self.type)

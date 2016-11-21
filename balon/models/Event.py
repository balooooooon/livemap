from balon import db


class Event(db.Model):
    joinTable = db.Table("param_event",
                         db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                         db.Column('parameter_id', db.Integer, db.ForeignKey('parameter.id'))
                         )

    class ValueEntry:
        TABLE_NAME = "event"

        KEY_ID = "id"
        KEY_TYPE = "type"
        KEY_TIME_CREATED = "time_created"
        KEY_FLIGHT_ID = "flight_id"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    time_created = db.Column(db.DateTime)
    parameters = db.relationship('Parameter', secondary=joinTable,
                                 backref=db.backref('parameter', lazy='dynamic'))

    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))


    def __init__(self, type, time_created):
        self.type = type
        self.time_created = time_created
        self.parametersDict = None

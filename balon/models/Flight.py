from balon import db


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    hash = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    parameters = db.relationship('Parameter', backref="flight", lazy='dynamic')

    class FlightEntry:
        TABLE_NAME = "flight"
        KEY_ID = "id"
        KEY_NUMBER = "number"
        KEY_hash = "hash"
        KEY_START_DATE = "start_date"

    def __init__(self, number, hash, date):
        self.number = number
        self.hash = hash
        self.start_date = date

    def __str__(self):
        return '<Flight [%d] [%d] %d / %s  >' % (self.id, self.start_date, self.number, self.hash)

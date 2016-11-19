
class Flight():

    class FlightEntry():
        KEY_ID = "id"
        KEY_NUMBER = "number"
        KEY_HASH = "hash"
        KEY_START_DATE = "start_date"
        TABLE_NAME = "flights"

    def __init__(self, number, hash, date):
        self.id = 0
        self.number = number
        self.hash = hash
        self.start_date = date

    def __str__(self):
        return '<Flight [%d] [%d] %s / %s  >' % (self.id, self.start_date, self.number, self.hash)
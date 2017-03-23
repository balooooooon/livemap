from balon import app
from tests.BalonTestCase import BalonTestCase

from balon.database import DBService
from balon.models.Flight import Flight
from datetime import datetime


class TestCase_DBService(BalonTestCase):
    def test_saveFlight_positive(self):
        date = datetime.now()
        number = 42
        hash = 'a1d0c6e83f027327d8461063f4ac58a6'
        flight = Flight(number=number, hash=hash, start_date=date)
        flight.id = DBService.saveFlight(flight)

        self.assertIsNotNone(flight.id)

    def test_getFlightByKey_number(self):
        date = datetime.now()
        number = 42
        hash = 'a1d0c6e83f027327d8461063f4ac58a6'
        flight = Flight(number=number, hash=hash, start_date=date)
        flight.id = DBService.saveFlight(flight)

        result = DBService.getFlightByKey(Flight.FlightEntry.KEY_NUMBER,42)
        result2 = DBService.getFlightByKey(Flight.FlightEntry.KEY_NUMBER,42)
        print(result)
        print(result2)
        self.assertEqual(result.id,flight.id)
        self.assertEqual(result.id,result2.id)

    def test_getFlightById_null(self):
        flight_id = 10000
        f = DBService.getFlightById(flight_id)
        self.assertIsNone(f)

    def test_getFlightById_exists(self):
        date = datetime.now()
        number = 42
        hash = 'a1d0c6e83f027327d8461063f4ac58a6'
        flight = Flight(number=number, hash=hash, start_date=date)
        flight.id = DBService.saveFlight(flight)

        result = DBService.getFlightById(flight.id)
        self.assertEqual(flight.id,result.id)

    def test_getFlightAll_one(self):
        f1 = Flight(number=42,hash='a1d0c6e83f027327d8461063f4ac58a6',start_date=datetime.now())
        f2 = Flight(number=43,hash='a1d0c6e83f027327d8461063f4ac58a6',start_date=datetime.now())
        f3 = Flight(number=44,hash='a1d0c6e83f027327d8461063f4ac58a6',start_date=datetime.now())
        f1.id = DBService.saveFlight(f1)
        f2.id = DBService.saveFlight(f2)
        f3.id = DBService.saveFlight(f3)

        flights = DBService.getFlightAll()
        self.assertIsNotNone(flights)
        self.assertEqual(len(flights),3)

    def test_saveFlight_sameNumber(self):
        f1 = Flight(number=42, hash='a1d0c6e83f027327d8461063f4ac58a6', start_date=datetime.now())
        f2 = Flight(number=42, hash='a1d0c6e83f027327d8461063f4ac58a6', start_date=datetime.now())
        f1.id = DBService.saveFlight(f1)
        f2.id = DBService.saveFlight(f2)

        self.assertEqual(f2.id,False)

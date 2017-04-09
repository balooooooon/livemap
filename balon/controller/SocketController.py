from balon.controller.IBalloonSubject import IBalloonSubject
from balon import socketio, LOG

from balon.service import BalloonService as service
import time


class SocketController(IBalloonSubject):
    def notifyEvent(self, flight_id):
        pass

    def notify(self, flight_id):
        LOG.debug("SocketController")
        self.emitTelemetryUpdate(flight_id)

    def __init__(self):
        pass

    def emitTelemetryUpdate(self, flight_id):
        flight = service.getFlightById(flight_id)
        lastPosition = service.getFlightLastPosition(flight.number)

        msg = {
            "type": "balloonPath",
            "created": 0,
            "data": {
                "type": "path",
                "eventTime": 0,
                "mode": "append",
                "points": []
            }
        }

        p = {
            "time": time.mktime(lastPosition.time_received.timetuple()),
            "lat":lastPosition.values["lat"].value,
            "lng": lastPosition.values["lng"].value,
            "alt": lastPosition.values["alt"].value
        }

        msg["data"]["points"].append(p)

        socketio.emit('message', {'data': 'Triggered message from SocketController'}, room=flight_id, namespace="/map")
        socketio.emit('balloon_update', msg, room=flight_id, namespace="/map")
        LOG.debug("Room message emited.")

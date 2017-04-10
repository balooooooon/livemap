from flask_socketio import emit, join_room

from balon.controller import Controller
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
            "lat": lastPosition.values["lat"].value,
            "lng": lastPosition.values["lng"].value,
            "alt": lastPosition.values["alt"].value
        }

        msg["data"]["points"].append(p)

        socketio.emit('message', {'data': 'Triggered message from SocketController'}, room=flight_id, namespace="/map")
        socketio.emit('balloon_update', msg, room=flight_id, namespace="/map")
        LOG.debug("Room message emited.")


# -------- SOCKETS ---------

@socketio.on('my_event', namespace='/socket/')
def sendMessage():
    emit('message', {'data': 'my data'})


@socketio.on('connect', namespace='/socket/')
def test_connect():
    LOG.info("Connected.")
    emit('message', {'data': 'Connected to Socket'})
    LOG.debug("Message sent.")


@socketio.on('connect', namespace='/map')
def balloonUpdate():
    LOG.info("Client connected")
    emit('message', {'data': '[Server]: You have been connected.'})
    global thread


@socketio.on('join', namespace='/map')
def socket_join(data):
    LOG.debug(data["flight"])
    flightNumber = data["flight"]
    flight = Controller.getFlightByNumber(flightNumber)
    join_room(flight.id)
    # LOG.debug(flask_socketio.rooms())
    emit('message', {'data': 'Subscribed for flight #{}'.format(flightNumber)}, namespace="/map")

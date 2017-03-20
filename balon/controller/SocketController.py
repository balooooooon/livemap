from balon import socketio, LOG
from balon.controller.IBalloonSubject import IBalloonSubject


class SocketController(IBalloonSubject):
    def notify(self, flight_id):
        LOG.debug("SocketController")
        self.emitUpdate(flight_id)

    def __init__(self):
        pass

    def emitUpdate(self,flight_id):
        socketio.emit('message',{'data': 'Triggered message from SocketController'}, room=flight_id, namespace="/map")
        LOG.debug("Room message emited.")


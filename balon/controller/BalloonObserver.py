class BalloonObserver(object):
    def __init__(self):
        self.__subjects = []
        from balon.controller.SocketController import SocketController
        self.register(SocketController())
        from balon.controller.SocialController import SocialController
        self.register(SocialController())

    def register(self, subject):
        self.__subjects.append(subject)
        return True

    def unregister(self, subject):
        self.__subjects.remove(subject)
        return True

    def update(self, flight_id):
        for subject in self.__subjects:
            subject.notify(flight_id)
        return True

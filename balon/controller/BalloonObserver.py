class BalloonObserver(object):
    def __init__(self):
        self.__subjects = []

    def register(self, subject):
        """ Register new subject
        @param subject: New subject to register
        @type subject: IBalloonSubject
        """
        self.__subjects.append(subject)
        return True

    def unregister(self, subject):
        """ Unregister new subject
        @param subject: Subject
        @type subject: IBalloonSubject
        """
        self.__subjects.remove(subject)
        return True

    def update(self, flight_id):
        """ Observer will notify all subjects
        @param flight_id: Flight ID
        """
        for subject in self.__subjects:
            subject.notify(flight_id)
        return True

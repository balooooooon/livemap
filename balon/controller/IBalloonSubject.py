from abc import ABCMeta, abstractmethod


class IBalloonSubject(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, flight_id):
        raise NotImplementedError()
        pass

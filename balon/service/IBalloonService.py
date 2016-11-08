from abc import ABCMeta, abstractmethod

class IBalloonService(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def getCurrentParameter(name):
        pass
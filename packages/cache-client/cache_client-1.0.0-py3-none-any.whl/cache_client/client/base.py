from abc import ABCMeta, abstractmethod


class ClientBase(metaclass=ABCMeta):
    def __init__(name=None, config=None, **kwargs):
        pass

    @property
    def label(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.label

    @abstractmethod
    def connect(self):
        return NotImplemented

    @abstractmethod
    def get(self, sql=None):
        return NotImplemented

    @abstractmethod
    def init_period_auto_update(self):
        return NotImplemented

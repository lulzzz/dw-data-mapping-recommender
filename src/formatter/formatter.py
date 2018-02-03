from abc import abstractmethod


class Formatter(object):
    @abstractmethod
    def format(self, input):
        pass

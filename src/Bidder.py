from abc import ABC, abstractmethod

class Bidder(ABC):
    """ Abstract class for a real-time bidder. """

    @abstractmethod
    def getBidPrice(self, bidRequest):
        """ Computes the bid price for a given request. Must be implemented in subclass. """
        pass

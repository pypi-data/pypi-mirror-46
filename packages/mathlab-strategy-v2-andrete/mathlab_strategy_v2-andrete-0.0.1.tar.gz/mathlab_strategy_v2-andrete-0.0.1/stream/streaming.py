from abc import ABCMeta, abstractmethod


class Streaming(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, trade):
        raise NotImplementedError('start method need to be implemented')

    # TODO: calculate the indicators and run the strategy, return instructions.
    def run_cycle(self, one_period_data):
        return None

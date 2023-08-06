from .common import Parameters
from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, **kargs):
        params = Parameters()
        for key, value in kargs.items():
            params.set(key, value)

    @abstractmethod
    def on_tick(self):
        return NotImplemented

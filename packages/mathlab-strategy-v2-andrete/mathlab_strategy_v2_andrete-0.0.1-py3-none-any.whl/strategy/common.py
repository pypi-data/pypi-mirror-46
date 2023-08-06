from enum import Enum
from typing import Any, Type, List
from abc import abstractmethod
import pandas as pd

from .singleton import Singleton
from .ticker import Symbol


class Instruction():
    pass


class Instructions(Singleton):
    def __init__(self):
        self.instructions = []

    def add(self, instruction: Instruction):
        self.instructions.append(instruction)

    def get_all(self) -> list:
        return self.instructions

    def clear(self) -> None:
        self.instructions = []


class Parameters(Singleton):
    def __init__(self):
        self.parameters = {}

    def set(self, name: str, value: Any):
        print(name, value)
        self.parameters[name] = value

    def get(self, name: str):
        return self.parameters[name]

    def contains(self, name: str):
        return name in self.parameters.keys()


class ParameterFunc():
    def __call__(self, name: str, default: Any = None):
        if Parameters().contains(name):
            return Parameters().get(name)
        else:
            return default


Parameter = ParameterFunc()


class StatusEnv(Singleton):
    def __init__(self):
        self.envs = {}

    def set(self, name, value):
        self.envs[name] = value

    def get(self, name):
        return self.envs.get(name)

    def contains(self, name):
        return name in self.envs.keys()


class Status():
    def __init__(self, name: str, enum: List[str], init: str):
        self.name = name
        if not StatusEnv().contains(self.name):
            StatusEnv().set(self.name, init)

    def __is__(self, s: str) -> bool:
        return self.get() == s

    def __ne__(self, s) -> bool:
        if isinstance(s, str):
            return self.get() != s
        return NotImplemented

    def __eq__(self, s) -> bool:
        if isinstance(s, str):
            return self.get() == s
        return NotImplemented

    def set(self, s: str):
        StatusEnv().set(self.name, s)

    def get(self):
        return StatusEnv().get(self.name)


class Interval(Enum):
    RT = 0  # 'realtime'
    M1 = 1  # 'm1'
    M5 = 5  # 'm5'
    M10 = 10  # 'm10'
    M15 = 15  # 'm15'
    M30 = 30  # 'm30'
    Hour = 60  # 'h1'
    Day = 1440  # 'day'
    Week = 10080  # 'week'
    Constant = 9999999

    def __gt__(self, right):
        return self.value > right.value

    def __eq__(self, right):
        return self.value == right.value


class MarketType(Enum):
    Futures = 1
    Spot = 2

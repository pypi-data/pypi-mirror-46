from typing import Union

import numpy as np

from ..base import BaseQuantity


class Time(BaseQuantity):
    def __init__(self, system: str, name: str, value: Union[float, np.ndarray], to_base: float, from_base: float):
        super().__init__(system, name, 'Time', value, to_base=to_base, from_base=from_base)
        self.base = Second


class Second(Time):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Second', value, to_base=1, from_base=1)


class Millisecond(Time):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Millisecond', value, to_base=1 / 1000, from_base=1000)


class Nanosecond(Time):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Nanosecond', value, to_base=1 / 1000000, from_base=1000000)


class Minute(Time):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Minute', value, to_base=60, from_base=1 / 60)


class Hour(Time):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Hour', value, to_base=3600, from_base=1 / 3600)


if __name__ == '__main__':
    t = Second(3600)
    print(t)
    t = t.convert(Millisecond)
    print(t)
    t = t.convert(Nanosecond)
    print(t)
    t = t.convert(Minute)
    print(t)
    t = t.convert(Hour)
    print(t)

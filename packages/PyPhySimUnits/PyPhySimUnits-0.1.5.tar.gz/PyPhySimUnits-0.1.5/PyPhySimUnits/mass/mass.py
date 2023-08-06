from typing import Union

import numpy as np

from ..base import BaseQuantity


class Mass(BaseQuantity):
    def __init__(self, system: str, name: str, value: Union[float, np.ndarray], to_base: float, from_base: float):
        super().__init__(system, name, 'Time', value, to_base=to_base, from_base=from_base)
        self.base = Kilogram


class Kilogram(Mass):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Kilogram', value, to_base=1, from_base=1)


class Gram(Mass):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Gram', value, to_base=1 / 1000, from_base=1000)


class Milligram(Mass):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Milligram', value, to_base=1 / 1000000, from_base=1000000)


class Pound(Mass):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Pound (mass)', value, to_base=1 / 2.20462, from_base=2.20462)


class Slug(Mass):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Slug (mass)', value, to_base=14.59390, from_base=1 / 14.59390)

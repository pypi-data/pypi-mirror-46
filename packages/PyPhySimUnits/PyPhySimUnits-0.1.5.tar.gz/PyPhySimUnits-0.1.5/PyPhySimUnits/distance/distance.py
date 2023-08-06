from typing import Union

import numpy as np

from ..base import BaseQuantity


class Distance(BaseQuantity):
    def __init__(self, system: str, name: str, value: Union[float, np.ndarray], to_base: float, from_base: float):
        super().__init__(system, name, 'Distance', value, to_base=to_base, from_base=from_base)
        self.base = Meter


class Meter(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Meter', value, to_base=1, from_base=1)


class Centimeter(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Centimeter', value, to_base=1 / 100, from_base=100)


class Millimeter(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Millimeter', value, to_base=1 / 1000, from_base=1000)


class Micrometer(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Micrometer', value, to_base=1 / 1000000, from_base=1000000)


class Kilometer(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Kilometer', value, to_base=1000, from_base=1 / 1000)


class Inch(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Inch', value, to_base=1 / 39.3701, from_base=39.3701)


class Foot(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Foot', value, to_base=1 / 3.28084, from_base=3.28084)


class Yard(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Yard', value, to_base=1 / 1.09361, from_base=1.09361)


class Mile(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Mile', value, to_base=1 / 0.00062137, from_base=0.00062137)


class NauticalMile(Distance):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Nautical Mile', value, to_base=1 / 0.00053995, from_base=0.00053995)


if __name__ == '__main__':
    t = Meter(1000)
    print(t)
    t = t.convert(Centimeter)
    print(t)
    t = t.convert(Millimeter)
    print(t)
    t = t.convert(Micrometer)
    print(t)
    t = t.convert(Kilometer)
    print(t)
    t = t.convert(Inch)
    print(t)
    t = t.convert(Foot)
    print(t)
    t = t.convert(Yard)
    print(t)
    t = t.convert(Mile)
    print(t)
    t = t.convert(NauticalMile)

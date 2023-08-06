from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist
from .. import area
from .. import mass
from .. import timeunits as t


class Energy(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[mass.Mass, area.Area]],
                 denominator: List[Union[t.Time, t.Time]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Energy', numerator, denominator, value)
        self.base = Joule


class Joule(Energy):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Joules', [mass.Kilogram, area.MetersSquared], [t.Second, t.Second], value)


class MilliJoule(Energy):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('MilliJoules', [mass.Gram, area.MetersSquared], [t.Second, t.Second], value)


class KiloJoule(Energy):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('KiloJoules', [mass.Kilogram, area.MetersSquared], [t.Millisecond, t.Second], value)


if __name__ == '__main__':
    e = Joule(1)
    print(e)
    e = e.convert(MilliJoule)
    print(e)
    e = e.convert(KiloJoule)
    print(e)

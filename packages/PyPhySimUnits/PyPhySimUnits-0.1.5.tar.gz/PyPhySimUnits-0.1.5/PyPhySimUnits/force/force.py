from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist
from .. import mass
from .. import timeunits as t


class Force(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[mass.Mass, dist.Distance]],
                 denominator: List[Union[t.Time, t.Time]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Force', numerator, denominator, value)
        self.base = Newton


class Newton(Force):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Newton', [mass.Kilogram, dist.Meter], [t.Second, t.Second], value)


class Poundal(Force):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Poundal', [mass.Pound, dist.Foot], [t.Second, t.Second], value)


class PoundForce(Force):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Pound-Force', [mass.Slug, dist.Foot], [t.Second, t.Second], value)


if __name__ == '__main__':
    e = Newton(1)
    print(e)
    e = e.convert(Poundal)
    print(e)
    e = e.convert(PoundForce)
    print(e)

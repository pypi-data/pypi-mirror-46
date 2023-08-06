from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist
from .. import timeunits  as t


class Acceleration(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[dist.Distance],
                 denominator: List[Union[t.Time, t.Time]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Acceleration', numerator, denominator, value)
        self.base = MetersPerSecondSquared


class MetersPerSecondSquared(Acceleration):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Meters per Second Squared', [dist.Meter], [t.Second, t.Second], value)


class MillimetersPerSecondSquared(Acceleration):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Millimeters per Second Squared', [dist.Millimeter], [t.Second, t.Second], value)


class FeetPerSecondSquared(Acceleration):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Feet per Second Squared', [dist.Foot], [t.Second, t.Second], value)


class MilesPerHourSecond(Acceleration):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Miles per Hour Second', [dist.Mile], [t.Hour, t.Second], value)


if __name__ == '__main__':
    acc = MetersPerSecondSquared(10)
    print(acc)
    acc = acc.convert(FeetPerSecondSquared)
    print(acc)
    acc = acc.convert(MilesPerHourSecond)
    print(acc)
    acc = acc.convert(MillimetersPerSecondSquared)
    print(acc)

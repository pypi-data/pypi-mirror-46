from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist
from .. import timeunits as t


class Speed(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[dist.Distance],
                 denominator: List[t.Time],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Speed', numerator, denominator, value)
        self.base = MetersPerSecond


class MetersPerSecond(Speed):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Meters per Second', [dist.Meter], [t.Second], value)


class FeetPerSecond(Speed):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Feet per Second', [dist.Foot], [t.Second], value)


class MilesPerHour(Speed):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Miles per Hour', [dist.Mile], [t.Hour], value)


class Knots(Speed):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Knots', [dist.NauticalMile], [t.Hour], value)


class KilometersPerHour(Speed):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Kilometers per Hour', [dist.Kilometer], [t.Hour], value)


if __name__ == '__main__':
    spd = MetersPerSecond(1)
    print(spd)
    spd = spd.convert(Knots)
    print(spd)
    spd = spd.convert(KilometersPerHour)
    print(spd)
    spd = spd.convert(MilesPerHour)
    print(spd)
    assert abs(spd.value - 2.236932) < 0.001

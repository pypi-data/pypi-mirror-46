from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist
from .. import area


class Volume(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[area.Area, dist.Distance]],
                 denominator: List[None],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Volume', numerator, denominator, value)
        self.base = MetersCubed


class MetersCubed(Volume):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Meters Cubed', [area.MetersSquared, dist.Meter], [], value)


class CentimetersCubed(Volume):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Centimeters Cubed', [area.CentimetersSquared, dist.Centimeter], [], value)


class MillimetersCubed(Volume):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Millimeters Cubed', [area.MillimetersSquared, dist.Millimeter], [], value)


class FeetCubed(Volume):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Feet Cubed', [area.FeetSquared, dist.Foot], [], value)


class InchesCubed(Volume):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Inches Cubed', [area.InchesSquared, dist.Inch], [], value)


if __name__ == '__main__':
    a = MetersCubed(0.002)
    print(a)
    a = a.convert(MillimetersCubed)
    print(a)
    a = a.convert(FeetCubed)
    print(a)
    a = a.convert(InchesCubed)
    print(a)

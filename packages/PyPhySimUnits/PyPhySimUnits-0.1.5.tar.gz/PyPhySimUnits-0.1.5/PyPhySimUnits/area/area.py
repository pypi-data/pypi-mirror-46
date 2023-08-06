from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import distance as dist


class Area(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[dist.Distance, dist.Distance]],
                 denominator: List[None],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Area', numerator, denominator, value)
        self.base = MetersSquared


class MetersSquared(Area):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Meters Squared', [dist.Meter, dist.Meter], [], value)


class CentimetersSquared(Area):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Centimeters Squared', [dist.Centimeter, dist.Centimeter], [], value)


class MillimetersSquared(Area):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Millimeters Squared', [dist.Millimeter, dist.Millimeter], [], value)


class InchesSquared(Area):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Inches Squared', [dist.Inch, dist.Inch], [], value)


class FeetSquared(Area):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Feet Squared', [dist.Foot, dist.Foot], [], value)


if __name__ == '__main__':
    a = MetersSquared(2)
    print(a)
    a = a.convert(MillimetersSquared)
    print(a)
    a = a.convert(FeetSquared)
    print(a)

from typing import List, Union

import numpy as np



from ..base import BaseQuantity, DerivedQuantity
from .. import mass
from .. import volume as vol


class Density(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[mass.Mass],
                 denominator: List[vol.Volume],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Density', numerator, denominator, value)
        self.base = KilogramsPerCubicMeter


class KilogramsPerCubicMeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Kilograms Per Cubic Meters', [mass.Kilogram], [vol.MetersCubed], value)


class GramsPerCubicMeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Grams Per Cubic Meters', [mass.Gram], [vol.MetersCubed], value)


class KilogramsPerCubicCentimeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Kilograms Per Cubic Centimeter', [mass.Kilogram], [vol.CentimetersCubed], value)


class GramsPerCubicCentimeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Grams Per Cubic Centimeter', [mass.Gram], [vol.CentimetersCubed], value)


class GramsPerCubicMillimeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Grams Per Cubic Millimeters', [mass.Gram], [vol.MillimetersCubed], value)


class KilogramsPerCubicMillimeter(Density):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Kilograms Per Cubic Millimeters', [mass.Kilogram], [vol.MillimetersCubed], value)


if __name__ == '__main__':
    d = KilogramsPerCubicMeter(2)
    print(d)
    d = d.convert(GramsPerCubicMeter)
    print(d)
    d = d.convert(KilogramsPerCubicCentimeter)
    print(d)
    d = d.convert(GramsPerCubicCentimeter)
    print(d)
    d = d.convert(KilogramsPerCubicMillimeter)
    print(d)
    d = d.convert(GramsPerCubicMillimeter)
    print(d)

from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import area
from .. import energy
from .. import volume as vol


class EnergyDensity2D(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[energy.Energy]],
                 denominator: List[Union[area.Area]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, '2D Energy Density', numerator, denominator, value)
        self.base = JoulesPerSquareMM


class EnergyDensity3D(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[Union[energy.Energy]],
                 denominator: List[Union[vol.Volume]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, '3D Energy Density', numerator, denominator, value)
        self.base = JoulesPerCubicMM


class JoulesPerSquareMM(EnergyDensity2D):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Joules per Square mm', [energy.Joule], [area.MillimetersSquared], value)


class JoulesPerCubicMM(EnergyDensity2D):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Joules per Cubic mm', [energy.Joule], [vol.MillimetersCubed], value)


if __name__ == '__main__':
    ed = JoulesPerSquareMM(1)
    print(ed)
    ed = JoulesPerCubicMM(1)
    print(ed)

from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import power
from .. import distance as dist
from .. import temperature as temp

class ThermalConductivity(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[power.Power],
                 denominator: List[Union[dist.Distance, temp.Temperature]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Thermal Conductivity', numerator, denominator, value)
        self.base = WattPerMeterKelvin


class WattPerMeterKelvin(ThermalConductivity):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Watts per Meter•Kelvin', [power.Watt], [dist.Meter, temp.Kelvin], value)
        # TODO: special-case handling for units with temperatures, converting this to Celsius
        # instead of Kelvin shouldn't change values here, but the code will as currently written


class WattPerMillimeterKelvin(ThermalConductivity):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Watts per mm•Kelvin', [power.Watt], [dist.Millimeter, temp.Kelvin], value)


if __name__ == '__main__':
    k = WattPerMeterKelvin(10)
    print(k)
    k = k.convert(WattPerMillimeterKelvin)
    print(k)

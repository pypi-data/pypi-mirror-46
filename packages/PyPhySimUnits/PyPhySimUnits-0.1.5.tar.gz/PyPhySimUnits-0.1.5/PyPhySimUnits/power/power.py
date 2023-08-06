from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import energy
from .. import timeunits as t


class Power(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[energy.Energy],
                 denominator: List[t.Time],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Power', numerator, denominator, value)
        self.base = Watt


class Watt(Power):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Watts', [energy.Joule], [t.Second], value)


class KiloWatt(Power):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('KiloWatts', [energy.KiloJoule], [t.Second], value)


if __name__ == '__main__':
    p = Watt(100)
    print(p)
    p = p.convert(KiloWatt)
    print(p)
    p = p.convert(Watt)
    print(p)

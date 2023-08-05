
import numpy
import ctypes

from vosolvers.base import VitaOptimumBase
from vosolvers.base import Strategy


class VitaOptimumConstrained(VitaOptimumBase):
    """Base Constrained Global Optimization Method Class"""

    def __init__(self, fobj, dim, nfe, np, strategy):
        self._dim = dim
        self._nfe = nfe
        self._np = np
        self._strategy = strategy
        self._validate_constrained()
        VitaOptimumBase.__init__(self, fobj)

    def info(self):
        """Prints information about the algorithm to standard output"""
        self._info_lib()

    def _validate_constrained(self):
        if not isinstance(self._nfe, int):
            raise TypeError("The evaluations number must be a positive integer: %s" % self._nfe)
        if self._nfe < 100:
            raise ValueError("The evaluations number must be >= 100")

        if not isinstance(self._np, int):
            raise TypeError("The population size must be a positive integer")
        if self._nfe < 10:
            raise ValueError("The population size must be >= 10")

        if not isinstance(self._strategy, Strategy):
            raise TypeError("Wrong strategy")

        self._validate()

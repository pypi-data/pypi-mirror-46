
import numpy
import ctypes

from abc import abstractmethod

from vosolvers.base import VitaOptimumBase
from vosolvers.base import Strategy


class VitaOptimumMixed(VitaOptimumBase):
    """Base Mixed Global Optimization Method Class"""

    def __init__(self, fobj,
                 dc, lc, hc,
                 di, li, hi,
                 db, dp,
                 nfe, np,
                 fc, fi,
                 cCr, iCr, bCr,
                 cS, iS, bS, pS,
                 lf):
        self._dc = dc
        self._lc = lc
        self._hc = hc
        self._di = di
        self._li = li
        self._hi = hi
        self._db = db
        self._dp = dp
        self._nfe = nfe
        self._np = np
        self._fc = fc
        self._fi = fi
        self._cCr = cCr
        self._iCr = iCr
        self._bCr = bCr
        self._cS = cS
        self._iS = iS
        self._bS = bS
        self._pS = pS
        self._lf = lf
        self._validate_mixed()
        VitaOptimumBase.__init__(self, fobj)

    def info(self):
        """Prints information about the algorithm to standard output"""
        self._info_lib()

    def _validate_mixed(self):
        if not isinstance(self._nfe, int):
            raise TypeError("The evaluations number must be an integer: %s" % self._nfe)
        if self._nfe < 1:
            raise ValueError("The evaluations number must be >= 1")

        if not isinstance(self._np, int):
            raise TypeError("The population size must be an integer")
        if self._np < 1:
            raise ValueError("The population size must be >= 1")

        if not isinstance(self._cS, Strategy):
            raise TypeError("Wrong strategy cS: %s" % self._cS)
        if not isinstance(self._iS, Strategy):
            raise TypeError("Wrong strategy iS: %s" % self._iS)
        if not isinstance(self._bS, Strategy):
            raise TypeError("Wrong strategy bS: %s" % self._bS)
        if not isinstance(self._pS, Strategy):
            raise TypeError("Wrong strategy pS: %s" % self._pS)

        #TODO: validate other parameters

        self._validate()

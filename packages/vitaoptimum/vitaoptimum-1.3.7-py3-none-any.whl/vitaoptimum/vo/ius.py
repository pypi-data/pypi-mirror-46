
import ctypes
import numpy

from vitaoptimum.vo.unconstrained import VitaOptimumUnconstrained
from vitaoptimum.base import Strategy, Validation


class Ius(VitaOptimumUnconstrained):
    """Continuous Unconstrained Global Optimization Method"""

    def __init__(self, fobj, dim, low, high,
                 nfe=100, np=25, f=0.85, cr=0.4,
                 strategy=Strategy.rand2best):
        self._low = low
        self._high = high
        self._f = f
        self._cr = cr
        VitaOptimumUnconstrained.__init__(self, fobj, dim, nfe, np, strategy)

    def run(self, restarts=1, verbose=False):
        """Runs the algorithm"""

        xopt = numpy.zeros(self._dim, dtype=ctypes.c_int32)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_int32),
                                          ctypes.c_int32)

        self._lib.vitaOptimum_Ius.restype = ctypes.c_double
        self._lib.vitaOptimum_Ius.argtypes = [ctypes.c_bool,
                                              callback_type,
                                              ctypes.c_int32,
                                              self._array_1d_int,
                                              self._array_1d_int,
                                              ctypes.c_int32,
                                              ctypes.c_int32,
                                              ctypes.c_double,
                                              ctypes.c_double,
                                              ctypes.c_int32,
                                              self._array_1d_int,
                                              self._array_1d_double
                                              ]
        best = self._lib.vitaOptimum_Ius(verbose,
                                         callback_type(self._fobj),
                                         self._dim,
                                         self._low,
                                         self._high,
                                         self._nfe,
                                         self._np,
                                         self._f,
                                         self._cr,
                                         self._strategy.value,
                                         xopt,
                                         conv)
        return best, xopt, conv

    def info(self):
        self._lib.vitaOptimum_Ius_info()

    def _validate(self):
        Validation.lh(self._low, self._high, self._dim)
        Validation.cr(self._cr)
        Validation.f(self._f)

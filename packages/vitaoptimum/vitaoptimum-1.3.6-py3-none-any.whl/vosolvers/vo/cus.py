
import ctypes
import numpy

from vosolvers.vo.unconstrained import VitaOptimumUnconstrained
from vosolvers.base import Strategy


class Cus(VitaOptimumUnconstrained):
    """Continuous Unconstrained Global Optimization Method"""

    def __init__(self, fobj, dim, low, high,
                 nfe=100, np=25, f=0.85, cr=0.4,
                 strategy=Strategy.rand2best):
        self._low = low
        self._high = high
        self._f = f
        self._cr = cr
        VitaOptimumUnconstrained.__init__(self, fobj, dim, nfe, np, strategy)

    def run(self, restarts = 1, verbose=False):
        """Runs the algorithm"""

        xopt = numpy.zeros(self._dim, dtype=ctypes.c_double)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int)

        self._lib.vitaOptimum_Cus.restype = ctypes.c_double
        self._lib.vitaOptimum_Cus.argtypes = [ctypes.c_bool,
                                              callback_type,
                                              ctypes.c_int,
                                              self._array_1d_double,
                                              self._array_1d_double,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_double,
                                              ctypes.c_double,
                                              ctypes.c_int,
                                              self._array_1d_double,
                                              self._array_1d_double
                                             ]
        best = self._lib.vitaOptimum_Cus(verbose,
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

    def _info_lib(self):
        self._lib.vitaOptimum_Cus_info()

    def _validate(self):
        if not isinstance(self._low, numpy.ndarray):
            raise TypeError("The low boundary is not a multidimensional numpy array: %s", self._low)
        if len(self._low) != self._dim:
            raise ValueError("The low boundary size must be %d", self._dim)

        if not isinstance(self._high, numpy.ndarray):
            raise TypeError("The high boundary is not a multidimensional numpy array")
        if len(self._high) != self._dim:
            raise ValueError("The high boundary size must be %d", self._dim)

        if not isinstance(self._f, float):
            raise TypeError("The differentiation must be a positive floating-point number")
        if self._f <= 0:
            raise ValueError("The differentiation must be > 0")

        if not isinstance(self._cr, float):
            raise TypeError("The crossover number must be a positive floating-point number")
        if self._cr <= 0 or self._cr >= 1:
            raise ValueError("The crossover number must be in [0, 1]")

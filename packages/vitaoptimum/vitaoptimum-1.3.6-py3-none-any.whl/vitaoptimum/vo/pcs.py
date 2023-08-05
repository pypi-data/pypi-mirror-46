import ctypes
import numpy

from vitaoptimum.vo.constrained import VitaOptimumConstrained
from vitaoptimum.base import Strategy, Validation


class Pcs(VitaOptimumConstrained):
    """Permutation Constrained Global Optimization Method"""

    def __init__(self, fobj, dim, ng, nh,
                 nfe=100, np=25, lf=5,
                 strategy=Strategy.rand3dir, tol=0.001):
        self._lf = lf
        VitaOptimumConstrained.__init__(self, fobj, dim, nfe, np, strategy, ng, nh, tol)

    def run(self, restarts=1, verbose=False):
        """Runs the algorithm"""

        xopt = numpy.zeros(self._dim, dtype=ctypes.c_int)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)
        constr = numpy.zeros(self._ng + self._nh, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_int),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int)

        self._lib.vitaOptimum_Pcs.restype = ctypes.c_double
        self._lib.vitaOptimum_Pcs.argtypes = [ctypes.c_bool,          # verbose
                                              callback_type,          # fobj
                                              ctypes.c_int,           # D
                                              ctypes.c_int,           # ng
                                              ctypes.c_int,           # nh
                                              ctypes.c_int,           # nfe
                                              ctypes.c_int,           # NP
                                              ctypes.c_int,           # LF
                                              ctypes.c_int,           # Strategy
                                              ctypes.c_double,        # tol
                                              self._array_1d_int,     # xopt (out)
                                              self._array_1d_double,  # const (out)
                                              self._array_1d_double   # conv (out)
                                              ]
        best = self._lib.vitaOptimum_Pcs(verbose,
                                         callback_type(self._fobj),
                                         self._dim,
                                         self._ng,
                                         self._nh,
                                         self._nfe,
                                         self._np,
                                         self._lf,
                                         self._strategy.value,
                                         self._tol,
                                         xopt,
                                         constr,
                                         conv)
        return best, xopt, constr, conv

    def info(self):
        self._lib.vitaOptimum_Pcs_info()

    def _validate(self):
        Validation.lf(self._lf, self._dim)

import ctypes
import numpy

from vitaoptimum.voplus.mixed import VitaOptimumPlusMixed
from vitaoptimum.base import StrategyPlus


class Mus(VitaOptimumPlusMixed):
    """Mixed Unconstrained Global Optimization Method"""

    def __init__(self, fobj,
                 dc, lc, hc,
                 di, li, hi,
                 db, dp,
                 np=50,
                 cstrategy=StrategyPlus.bbest2pbest,
                 istrategy=StrategyPlus.cbest2pbest,
                 bstrategy=StrategyPlus.rrand2pbest,
                 pstrategy=StrategyPlus.cbest2pbest,
                 stagnation=1000,
                 qmeasures=numpy.zeros(4, dtype=ctypes.c_double)):
        VitaOptimumPlusMixed.__init__(self, fobj,
                                      dc, lc, hc,
                                      di, li, hi,
                                      db, dp,
                                      np,
                                      cstrategy,
                                      istrategy,
                                      bstrategy,
                                      pstrategy,
                                      stagnation,
                                      qmeasures)

    def run(self, restarts=1, verbose=False):
        """Runs the algorithm"""

        converged = numpy.zeros(1, dtype=ctypes.c_bool)
        xoptC = numpy.zeros(self._dc, dtype=ctypes.c_double)
        xoptI = numpy.zeros(self._di, dtype=ctypes.c_int)
        xoptB = numpy.zeros(self._db, dtype=ctypes.c_int)
        xoptP = numpy.zeros(self._dp, dtype=ctypes.c_int)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_double),  # xc
                                          ctypes.c_int,  # dc
                                          ctypes.POINTER(ctypes.c_int),  # xi
                                          ctypes.c_int,  # di
                                          ctypes.POINTER(ctypes.c_int),  # xb
                                          ctypes.c_int,  # db
                                          ctypes.POINTER(ctypes.c_int),  # xp
                                          ctypes.c_int)  # dp

        self._lib_plus.vitaOptimumPlus_Mus.restype = ctypes.c_double
        self._lib_plus.vitaOptimumPlus_Mus.argtypes = [
            callback_type,          # fobj
            self._array_1d_double,  # xoptC
            self._array_1d_int,     # xoptI
            self._array_1d_int,     # xoptB
            self._array_1d_int,     # xoptP
            ctypes.c_int32,         # dimC
            self._array_1d_double,  # lowC
            self._array_1d_double,  # highC
            ctypes.c_int32,         # dimI
            self._array_1d_int,     # lowI
            self._array_1d_int,     # highI
            ctypes.c_int32,         # dimB
            ctypes.c_int32,         # dimP
            ctypes.c_int32,         # np
            ctypes.c_int32,         # strategyC
            ctypes.c_int32,         # strategyI
            ctypes.c_int32,         # strategyB
            ctypes.c_int32,         # strategyP
            ctypes.c_int32,         # stagnation
            self._array_1d_bool,    # converged
            self._array_1d_double,  # qmeasures
            ctypes.c_bool  # verbose
        ]

        best = self._lib_plus.vitaOptimumPlus_Mus(
            callback_type(self._fobj),
            xoptC, xoptI, xoptB, xoptP,
            self._dc, self._lc, self._hc,
            self._di, self._li, self._hi,
            self._db, self._dp,
            self._np,
            self._cstrategy.value,
            self._istrategy.value,
            self._bstrategy.value,
            self._pstrategy.value,
            self._stagnation,
            converged,
            self._qmeasures,
            verbose)

        return best, xoptC, xoptI, xoptB, xoptP, converged, self._qmeasures

    def info(self):
        self._lib_plus.vitaOptimumPlus_Mus_info()

    def _validate(self):
        pass

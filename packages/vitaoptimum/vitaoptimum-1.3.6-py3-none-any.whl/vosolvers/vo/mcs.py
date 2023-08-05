
import ctypes
import numpy

from vosolvers.vo.mixed import VitaOptimumMixed


class Mcs(VitaOptimumMixed):
    """Mixed Constrained Global Optimization Method"""

    def __init__(self, fobj,
                 dc, lc, hc,
                 di, li, hi,
                 db, dp,
                 ng, nh,
                 nfe, np,
                 fc, fi,
                 cCr, iCr, bCr,
                 cS, iS, bS, pS,
                 lf, tol):
        self._ng = ng
        self._nh = nh
        self._tol = tol
        VitaOptimumMixed.__init__(self, fobj,
                                  dc, lc, hc,
                                  di, li, hi,
                                  db, dp,
                                  nfe, np,
                                  fc, fi,
                                  cCr, iCr, bCr,
                                  cS, iS, bS, pS,
                                  lf)

    def run(self, restarts = 1, verbose=False):
        """Runs the algorithm"""

        xoptC = numpy.zeros(self._dc, dtype=ctypes.c_double)
        xoptI = numpy.zeros(self._di, dtype=ctypes.c_int)
        xoptB = numpy.zeros(self._db, dtype=ctypes.c_int)
        xoptP = numpy.zeros(self._dp, dtype=ctypes.c_int)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)

        constr = numpy.zeros(self._ng + self._nh, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,                  # return
                                          ctypes.POINTER(ctypes.c_double),  # xc
                                          ctypes.c_int,                     # dc
                                          ctypes.POINTER(ctypes.c_int),     # xi
                                          ctypes.c_int,                     # di
                                          ctypes.POINTER(ctypes.c_int),     # xb
                                          ctypes.c_int,                     # db
                                          ctypes.POINTER(ctypes.c_int),     # xp
                                          ctypes.c_int,                     # dp
                                          ctypes.POINTER(ctypes.c_double),  # g
                                          ctypes.c_int,                     # ng
                                          ctypes.POINTER(ctypes.c_double),  # h
                                          ctypes.c_int)                     # nh
        self._lib.vitaOptimum_Mcs.restype = ctypes.c_double                 # best
        self._lib.vitaOptimum_Mcs.argtypes = [ctypes.c_bool,                # verbose
                                              callback_type,                # fobj
                                              ctypes.c_int,                 # Dc
                                              self._array_1d_double,        # Lc
                                              self._array_1d_double,        # Hc
                                              ctypes.c_int,                 # Di
                                              self._array_1d_int,           # Li
                                              self._array_1d_int,           # Hi
                                              ctypes.c_int,                 # Db
                                              ctypes.c_int,                 # Dp
                                              ctypes.c_int,                 # ng
                                              ctypes.c_int,                 # nh
                                              ctypes.c_int,                 # nfe
                                              ctypes.c_int,                 # Np
                                              ctypes.c_double,              # Fc
                                              ctypes.c_double,              # Fi
                                              ctypes.c_double,              # cCr
                                              ctypes.c_double,              # iCr
                                              ctypes.c_double,              # bCr
                                              ctypes.c_int,                 # cS
                                              ctypes.c_int,                 # iS
                                              ctypes.c_int,                 # bS
                                              ctypes.c_int,                 # pS
                                              ctypes.c_int,                 # LF
                                              ctypes.c_double,              # tol
                                              self._array_1d_double,        # xoptC
                                              self._array_1d_int,           # xoptI
                                              self._array_1d_int,           # xoptB
                                              self._array_1d_int,           # xoptP
                                              self._array_1d_double,        # constr
                                              self._array_1d_double         # conv
                                             ]

        best = self._lib.vitaOptimum_Mcs(verbose,
                                         callback_type(self._fobj),
                                         self._dc, self._lc, self._hc,
                                         self._di, self._li, self._hi,
                                         self._db, self._dp,
                                         self._ng, self._nh,
                                         self._nfe, self._np,
                                         self._fc, self._fi,
                                         self._cCr, self._iCr, self._bCr,
                                         self._cS.value, self._iS.value, self._bS.value, self._pS.value,
                                         self._lf,
                                         self._tol,
                                         xoptC, xoptI, xoptB, xoptP,
                                         constr, conv)
        return best, xoptC, xoptI, xoptB, xoptP, constr, conv

    def _info_lib(self):
        self._lib.vitaOptimum_Cus_info()

    def _validate(self):
        if not isinstance(self._ng, int):
            raise TypeError("The dimension constraint ng must be an integer")
        if self._ng <= 0:
            raise ValueError("The dimension constraint nh must be > 0")

        if not isinstance(self._nh, int):
            raise TypeError("The dimension constraint nh must be an integer")
        if self._nh <= 0:
            raise ValueError("The dimension constraint nh must be > 0")

        if not isinstance(self._tol, float):
            raise TypeError("The tolerance must be a float")
        if self._tol <= 0:
            raise ValueError("The tolerance must be > 0")


import ctypes
import numpy

from abc import abstractmethod
from enum import Enum
from sys import platform


class Strategy(Enum):
    rand3 = 1
    rand2best = 2
    rand3dir = 3
    rand2bestdir = 4


class VitaOptimumBase:
    def __init__(self, fobj):
        self._array_1d_double =\
            numpy.ctypeslib.ndpointer(dtype=ctypes.c_double, ndim=1, flags='F')
        self._array_1d_int =\
            numpy.ctypeslib.ndpointer(dtype=ctypes.c_int32, ndim=1, flags='F')
        self._set_fobj(fobj)
        self._load_vo()
        self._load_vo_plus()

    def _load_vo(self):
        if platform in ["linux", "linux2"]:  # Linux
            shared_object = "libvo.so"
        elif platform == "darwin":  # OS X
            shared_object = "libvo.so"
        elif platform == "win32":  # Windows
            shared_object = "vo.dll"
        else:
            shared_object = "libvo.so"
        self._lib = ctypes.PyDLL(shared_object, mode=ctypes.RTLD_GLOBAL)

    def _load_vo_plus(self):
        pass
    # TODO vo-plus load

    @property
    def fobj(self):
        return self._fobj

    @fobj.setter
    def fobj(self, value):
        self._set_fobj(value)

    def _set_fobj(self, value):
        if not value:
            raise AttributeError("The objective function is not defined")
        if not callable(value):
            raise TypeError("The objective function is not callable")
        self._fobj = value

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def run(self, restarts, verbose):
        pass

    @abstractmethod
    def _validate(self):
        pass


class Validation:

    @staticmethod
    def nfe(nfe, np):
        if not isinstance(nfe, int):
            raise TypeError("The number of function evaluations nfe must be a positive integer: %s" % nfe)
        if nfe < np:
            raise ValueError("The number of function evaluations nfe must be >= %d" % np)

    @staticmethod
    def np(np):
        if not isinstance(np, int):
            raise TypeError("The population size np must be a positive integer")
        if np < 5:
            raise ValueError("The population size np must be >= 5")

    @staticmethod
    def strategy(strategy):
        if not isinstance(strategy, Strategy):
            raise TypeError("Wrong strategy")

    @staticmethod
    def f(f):
        if not isinstance(f, float):
            raise TypeError("The differentiation parameter must be a floating-point number")
        if f < 0:
            raise ValueError("The differentiation parameter must be >= 0")

    @staticmethod
    def cr(cr):
        if not isinstance(cr, float):
            raise TypeError("The crossover parameter must be a floating-point number")
        if cr < 0 or cr >= 1:
            raise ValueError("The crossover parameter must be in [0, 1)")

    @staticmethod
    def lf(lf, dim):
        if not isinstance(lf, int):
            raise TypeError("The locality factor must be an integer")
        if lf <= 0:
            raise ValueError("The locality factor must be a positive number")
        if lf >= dim:
            raise ValueError("The locality factor must be less than dimension %d", dim)

    @staticmethod
    def dim(dim):
        if not isinstance(dim, int):
            raise TypeError("The dimension must be an integer")
        if dim < 0:
            raise ValueError("The dimension must be >= 0")

    @staticmethod
    def lh(low, high, dim):
        if not isinstance(low, numpy.ndarray):
            raise TypeError("The low boundary is not a multidimensional numpy array: %s", low)
        if len(low) != dim:
            raise ValueError("The low boundary size must be %d", dim)

        if not isinstance(high, numpy.ndarray):
            raise TypeError("The high boundary is not a multidimensional numpy array")
        if len(high) != dim:
            raise ValueError("The high boundary size must be %d", dim)

    @staticmethod
    def ng(ng):
        if not isinstance(ng, int):
            raise TypeError("The inequality constraints dimension ng must be an integer")
        if ng < 0:
            raise ValueError("The inequality constraints dimension ng must be >= 0")

    @staticmethod
    def nh(nh):
        if not isinstance(nh, int):
            raise TypeError("The equality constraints dimension nh must be an integer")
        if nh < 0:
            raise ValueError("The equality constraints dimension nh must be >= 0")

    @staticmethod
    def tol(tol):
        if not isinstance(tol, float):
            raise TypeError("The tolerance must be a float")
        if tol <= 0:
            raise ValueError("The tolerance must be > 0")
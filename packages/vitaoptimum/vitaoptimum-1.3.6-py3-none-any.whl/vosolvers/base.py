
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
    def _info_lib(self):
        pass

    @abstractmethod
    def run(self, restarts, verbose):
        pass

    @abstractmethod
    def _validate(self):
        pass

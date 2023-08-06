#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from dateutil.parser import parse

class WrangleFloat(object):
    """transform every element within a numpy array into float object.
    """
    def __init__(self, default=np.nan):
        self.default = default
        self._func = np.vectorize(self._wrangle)

    def _wrangle(self, x):
        if x == "":
            return self.default
        else:
            return float(x)

    def __call__(self, np_arr):
        try:
            return self._func(np_arr) if np_arr.shape[0] != 0 else np_arr
        except:
            raise Exception("WrangleFloat encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))


class WrangleStr(object):
    """transform every element within a numpy array into string object.
    """
    def __init__(self, default=np.nan):
        self.default = default
        self._func = np.vectorize(self._wrangle)

    def _wrangle(self, x):
        if x == "":
            return self.default
        else:
            return str(x)

    def __call__(self, np_arr):
        try:
            return self._func(np_arr) if np_arr.shape[0] != 0 else np_arr
        except:
            raise Exception("WrangleStr encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class WrangleNormalDatetime(object):
    """transform every element within a numpy array into datetime object.
    """
    def __init__(self, default=np.nan):
        self.default = default
        self._func = np.vectorize(self._wrangle)

    def _wrangle(self, x):
        if x == "":
            return self.default
        else:
            return parse(str(x))

    def __call__(self, np_arr):
        try:
            return self._func(np_arr) if np_arr.shape[0] != 0 else np_arr
        except:
            raise Exception("WrangleNormalDatetime encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

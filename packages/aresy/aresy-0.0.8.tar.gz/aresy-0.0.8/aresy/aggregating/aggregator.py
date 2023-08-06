#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Sum(object):
    """sum a numpy arrray.
    """
    def __init__(self, default=np.nan):
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.sum(np_arr) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Sum encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class Mean(object):
    """get mean of a numpy arrray.
    """
    def __init__(self, default=np.nan):
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.mean(np_arr) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Mean encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class Std(object):
    """get mean of a numpy arrray.
    """
    def __init__(self, default=np.nan):
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.std(np_arr) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Std encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class Max(object):
    """get max of a numpy arrray.
    """
    def __init__(self, default=np.nan):
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.max(np_arr) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Max encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class Min(object):
    """get max of a numpy arrray.
    """
    def __init__(self, default=np.nan):
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.min(np_arr) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Min encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

class Quantile(object):
    """get max of a numpy arrray.
    """
    def __init__(self, q, interpolation='linear', default=np.nan):
        self.q = q
        self.interpolation = interpolation
        self.default = default

    def __call__(self, np_arr):
        try:
            return np.percentile(np_arr, self.q, interpolation=self.interpolation) if np_arr.shape[0] != 0 else self.default
        except:
            raise Exception("Quantile encounters unexpected error need hot-fixing, the data you are dealing with is: \n{0}\n".format(np_arr))

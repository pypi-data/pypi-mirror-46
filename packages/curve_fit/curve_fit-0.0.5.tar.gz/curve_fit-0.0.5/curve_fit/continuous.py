# -*- coding: utf-8 -*-
# @Project : curve_fit
# @Time    : 2019-05-27 14:51
# @Author  : Samuel Chan
# @Email   : samuelchan1205@gmail.com
# @File    : continuous.py


import pickle
import numpy as np
from patsy import dmatrix
import statsmodels.api as sm


class Continuous:
    def __init__(self, k=3):
        self.model = None
        self.all = None
        self.k = k

    def _transform(self, x):
        n = x.shape[0]
        if self.all is None:
            self.all = np.array(x)
        else:
            self.all = np.concatenate([self.all, x])
        transformed_x = dmatrix("cr(x,df={})".format(self.k), {"x": self.all}, return_type='dataframe')[-n:]
        return transformed_x

    def fit(self, x, y):
        x = np.array(x)
        y = np.array(y)
        assert x.ndim == 1
        assert x.shape == y.shape
        trans_x = self._transform(x)
        self.model = sm.GLM(y, trans_x).fit()
        return self.model

    def predict(self, x):
        x = np.array(x)
        trans_x = self._transform(x)
        pred = self.model.predict(trans_x)
        return pred

    def save(self, dir):
        with open(dir, "wb") as fw:
            pickle.dump(self.model, fw)

    def load(self, dir):
        with open(dir, "rb") as fr:
            self.model = pickle.load(fr)

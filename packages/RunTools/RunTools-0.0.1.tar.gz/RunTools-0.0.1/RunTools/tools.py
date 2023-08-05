# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 14:32
# @Author   : Run 
# @File     : tools.py
# @Software : PyCharm

import numpy as np
import pandas as pd
from string import ascii_lowercase
import time


def gen_df(lb, ub, shape):
    """

    :param lb: lower bound
    :param ub: upper bound
    :param shape: (m, n)
    :return:
    """
    data = np.random.randint(lb, ub, shape)
    cols = list(ascii_lowercase[:shape[1]])
    df = pd.DataFrame(data, columns=cols)
    print("shape:", df.shape)
    print(df.head(2))
    return df


def timer(func):
    """
    a decorator for timing
    old function results         new function results
    r1, r2, ..., rn       ->     (r1, r2, ..., rn), cost_time

    :param func:
    :return:
    """

    def dec(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        cost_t = t2 - t1
        if cost_t < 1:  # 耗时低于1s重复10遍
            n = 10
        elif cost_t < 10:  # 耗时低于10s重复5遍
            n = 5
        else:  # 耗时超过10s，不进行重复试验
            n = 1
            #
        for _ in range(n - 1):
            t1 = time.time()
            res = func(*args, **kwargs)
            t2 = time.time()
            cost_t += t2 - t1
        cost_t /= n
        print("{0} cost time: {1}s, {2} loops".format(func.__name__, t2 - t1, n))
        return res

    return dec


def flatten_lists(lists):
    """
    [(x_1, ..., x_n), ..., [y_1, ..., y_m], ..., z1, z2, ...] -> [x_1, ..., x_n, ..., y_1, ..., y_m, ..., z1, z2, ...]
    :param lists:
    :return:
    """
    l = []
    for item in lists:
        if type(item) in {tuple, set, list}:
            l += list(item)
        else:
            l.append(item)
    return l










import numpy as np
import pandas as pd
from tidyframe import apply_cum

series = np.random.randint(1, 6, 10)

cum_func = lambda x, y: x * y
judge_func = lambda x: x > 10

series = range(3, 8)


def test_apply_cum_basic():
    apply_cum(series, cum_func, init_value=1)


def test_apply_cum_judge_func():
    df = apply_cum(pd.Series(series),
                   cum_func,
                   judge_func=lambda x: x > 30,
                   init_value=1)
    assert df['index_first'][0] and df['index_first'][
        3], 'index_first is not work'
    assert df['index_last'][2], 'index_last is not work'


def test_apply_cum_judge_func_2():
    series = [10, 2, 3, 6, 3]
    df = apply_cum(series, judge_func=lambda x: x > 9)
    assert df['index_first'][0] and df['index_last'][
        0], 'first value of index_first and index_last is not True'

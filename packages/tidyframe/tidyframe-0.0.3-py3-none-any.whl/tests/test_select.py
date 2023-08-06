from tidyframe import tools
import pandas as pd
import numpy as np

df = pd.DataFrame(np.array(range(10)).reshape(2, 5),
                  columns=list('abcde'),
                  index=['row_1', 'row_2'])


def test_select_basic():
    assert tools.select(df,
                        columns=['b', 'd'
                                 ]).shape[1] == 2, 'select column must equal 2'


def test_select_columns_minus():
    assert tools.select(
        df, columns_minus=['b',
                           'd']).shape[1] == 3, 'select column must equal 3'


def test_select_deepcopy():
    assert tools.select(df, columns_minus=['b', 'd'],
                        copy=True).shape[1] == 3, 'select column must equal 3'


def test_select_columns_minus():
    assert tools.select(
        df, columns_minus=['b',
                           'd']).shape[1] == 3, 'select column must equal 3'


def test_select_columns_between():
    assert tools.select(
        df, columns_between=['b',
                             'd']).shape[1] == 3, 'select column must equal 3'


def test_select_pattern():
    assert tools.select(
        df, pattern='[a|b]').shape[1] == 2, 'select column must equal 2'


def test_select_pattern_list():
    assert tools.select(df,
                        pattern=['[a|b]', '[c|d]'
                                 ]).shape[1] == 4, 'select column must equal 4'

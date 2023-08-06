import pandas as pd
from tidyframe import add_columns


def test_add_columns_basic():
    df = pd.DataFrame()
    df['a'] = [1, 6]
    df['b'] = [2, 7]
    df['c'] = [3, 8]
    df['d'] = [4, 9]
    df['e'] = [5, 10]
    add_columns(df, columns=['a', 'f'])
    assert df.shape[1] == 6, "add column error"


def test_add_columns_basic2():
    df = pd.DataFrame()
    df['a'] = [1, 6]
    df['b'] = [2, 7]
    df['c'] = [3, 8]
    df['d'] = [4, 9]
    df['e'] = [5, 10]
    add_columns(df, columns=['a', 'f'], default=[30, [10, 11]])
    assert df.shape[1] == 6, "add column error"


def test_add_columns_deepcopy():
    df = pd.DataFrame()
    df['a'] = [1, 6]
    df['b'] = [2, 7]
    df['c'] = [3, 8]
    df['d'] = [4, 9]
    df['e'] = [5, 10]
    df_return = add_columns(
        df, columns=['a', 'f'], default=[30, [10, 11]], deepcopy=False)
    assert df.shape[1] == 6, "add_columns deepcopy error"

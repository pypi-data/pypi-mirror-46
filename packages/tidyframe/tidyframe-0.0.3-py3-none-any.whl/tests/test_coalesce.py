import pandas as pd
from tidyframe import coalesce


def test_coalesce_basic():
    df = pd.DataFrame()
    df['a'] = [None, pd.np.NaN, pd.np.nan, pd.np.nan]
    df['b'] = [None, 4, 6, pd.np.nan]
    df['c'] = [None, pd.np.NaN, 6, pd.np.nan]
    coalesce(df, ['a', 'b', 'c'], default_value=10)

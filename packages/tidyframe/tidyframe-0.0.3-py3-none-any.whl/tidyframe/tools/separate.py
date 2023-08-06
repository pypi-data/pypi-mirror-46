""" Separate string list to Pandas DataFrame """

import pandas as pd
import numpy as np
from .select import select_index


def separate(series, index=None, columns=None, otherwise=np.NaN):
    """
    Separate string list to Pandas DataFrame

    Parameters
    ----------
    series : list of list or Series of list
    index : filter return index
    columns : return column name of DataFrame
    otherwise : numpy.NaN, fill value of not exist value

    Returns
    -------
    Pandas DataFrame with split each element of series to column

    Examples
    --------
    >>> from tidyframe.tools import separate
    >>> df = pd.DataFrame({'full_string': ['a b c d e z', 'f g h i']},
    ...                   index=['row_1', 'row_2'])
    >>> series = df.full_string.str.split(' ')
    >>> separate(series)
        col_0 col_1 col_2 col_3 col_4 col_5
    row_1     a     b     c     d     e     z
    row_2     f     g     h     i   NaN   NaN
    """
    series = pd.Series(series)
    ncol = series.apply(len).max()
    if index is not None:
        assert max(index) < ncol, 'max of index MUST less than max of Series'
        if columns is not None:
            assert len(columns) == len(
                index), "length of columns MUST SAME as length of index"
        else:
            columns = pd.Series(
                ['col'] * len(index)) + '_' + pd.Series(index).apply(str)
    else:
        index = list(range(ncol))
        columns = pd.Series(['col'] * ncol) + '_' + pd.Series(
            range(ncol)).apply(str)
    return_df = pd.DataFrame()

    for i, name in zip(index, columns):
        return_df[name] = series.apply(lambda x: select_index(x, i, otherwise))
    return return_df

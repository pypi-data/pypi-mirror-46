""" Easy Select Column Method from Pandas DataFrame """

import re
import numpy as np
from copy import copy, deepcopy
from funcy import chunks


def select(df,
           columns=None,
           columns_minus=None,
           columns_between=None,
           pattern=None,
           copy=False):
    """
    Select Pandas DataFrame Columns

    Parameters
    ----------
    df : Pandas DataFrame
    columns_minus : column which want to remove
    columns_between: list with two element, select columns bwtween two columns
    pattern: regular expression or list of regular expression, return match columns
    copy : whether return deep copy DataFrame

    Returns
    -------
    Pandas DataFrame

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from tidyframe import select
    >>> df = pd.DataFrame(np.array(range(10)).reshape(2, 5),
    ...                   columns=list('abcde'),
    ...                   index=['row_1', 'row_2'])
    >>> select(df, columns=['b', 'd'])
        b  d
    row_1  1  3
    row_2  6  8
    >>> select(df, columns_minus=['b', 'd'])
        a  c  e
    row_1  0  2  4
    row_2  5  7  9
    >>> select(df, pattern='[a|b]')
        a  b
    row_1  0  1
    row_2  5  6
    """
    if columns:
        df_return = df[columns]
    if columns_minus:
        raw_col = {value: i for i, value in enumerate(df.columns)}
        for pop_key in columns_minus:
            raw_col.pop(pop_key)
        df_return = df[list(raw_col.keys())]
    if columns_between:
        columns_location = {column: i for i, column in enumerate(df.columns)}
        assert columns_location[columns_between[0]] < columns_location[
            columns_between[
                1]], 'first column location must less than second column location'
        df_return = df.iloc[:,
                            range(columns_location[columns_between[0]],
                                  columns_location[columns_between[1]] + 1)]
    if pattern and isinstance(pattern, str):
        columns_want = list(filter(lambda x: re.search(pattern, x),
                                   df.columns))
        df_return = df[columns_want]
    if pattern and isinstance(pattern, list):
        columns_want = []
        for each_pattern in pattern:
            columns_want.extend(
                list(filter(lambda x: re.search(each_pattern, x), df.columns)))
            columns_want = list(set(columns_want))
            columns_want.sort()
            df_return = df[columns_want]

    if copy:
        return deepcopy(df_return)
    else:
        return df_return


def reorder_columns(df, columns=None, pattern=None, last_columns=None):
    """
    reorder columns of pandas DataFrame

    Parameters
    ----------
    df : Pandas DataFrame
    columns : list which want to head column name(non-use if pattern is not None)
    pattern : regular expression pattern which let selected columns be at head columns
    last_columns : list which want to last column name

    Returns
    -------
    Pandas DataFrame

    Examples
    --------
    >>> import pandas as pd
    >>> from tidyframe import reorder_columns
    >>> df = pd.DataFrame([{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 2}])
    >>> df_reorder = reorder_columns(df, ['b', 'c'], last_columns=['a', 'd'])
    >>> df_reorder
    b  c  e  a  d
    0  1  1  2  1  1
    """
    if pattern:
        reorder_columns = list(
            filter(lambda x: re.search(pattern, x), df.columns))
    else:
        reorder_columns = copy(list(columns))
        reorder_columns = [x for x in columns if df.columns.contains(x)]
    raw_columns = df.columns.copy()
    if last_columns:
        center_columns = raw_columns.difference(reorder_columns).difference(
            last_columns).tolist()
    else:
        center_columns = raw_columns.difference(reorder_columns).tolist()
    reorder_columns.extend(center_columns)
    if last_columns:
        reorder_columns.extend(last_columns)
    return df[reorder_columns]


def get_batch_dataframe(df, batch_size=100):
    """
    split DataFrame to sub-DataDrame and each sub-DataDrame row size is batch_size

    Parameters
    ----------
    df : Pandas DataFrame
    batch_size : number of records in each sub-dataframe(default: 100)

    Returns
    -------
    DataFrame generator

    Examples
    --------
    >>> import pandas as pd
    >>> from tidyframe import get_batch_dataframe
    >>> df = pd.DataFrame()
    >>> df['col_1'] = list("abcde")
    >>> df['col_2'] = [1, 2, 3, 4, 5]
    >>> dfs = [ x for x in get_batch_dataframe(df,2)]
    >>> dfs[-1]
        col_1  col_2
    4       e      5
    >>> [ x.shape[0] for x in dfs]
    [2, 2, 1]
    """
    for min_batch in chunks(batch_size, range(df.shape[0])):
        yield df.iloc[min_batch, :]


def select_index(x, i, otherwise=np.NaN):
    """
    Select by index and Catch all Exception

    Parameters
    ----------
    x : array
    i : index
    otherwise : fill value if exist exception

    Returns
    -------
    x[i] if not exception happen else return otherwise
    """
    try:
        return x[i]
    except:
        return otherwise
""" All combination rows from list of DataFrame """

import pandas as pd


def combination(dfs):
    """
    All combination rows from list of DataFrame

    Parameters
    ----------
    dfs : list of Pandas DataFrame

    Returns
    -------
    Pandas DataFrame

    Examples
    --------
    >>> import pandas as pd
    >>> from tidyframe import combination
    >>> df_a = pd.DataFrame({'a1': list('ABC'), 'a2': list('CDE')})
    >>> df_b = pd.DataFrame({'b1': list('01234'), 'b2': list('56789')})
    >>> df_c = pd.DataFrame({'c1': list('pq'), 'c2': list('rs')})
    >>> combination([df_a, df_b, df_c])
        index_0 a1 a2  index_1 b1 b2  index_2 c1 c2
    0         0  A  C        0  0  5        0  p  r
    1         0  A  C        0  0  5        1  q  s
    2         0  A  C        1  1  6        0  p  r
    3         0  A  C        1  1  6        1  q  s
    4         0  A  C        2  2  7        0  p  r
    5         0  A  C        2  2  7        1  q  s
    6         0  A  C        3  3  8        0  p  r
    7         0  A  C        3  3  8        1  q  s
    8         0  A  C        4  4  9        0  p  r
    9         0  A  C        4  4  9        1  q  s
    10        1  B  D        0  0  5        0  p  r
    11        1  B  D        0  0  5        1  q  s
    12        1  B  D        1  1  6        0  p  r
    13        1  B  D        1  1  6        1  q  s
    14        1  B  D        2  2  7        0  p  r
    15        1  B  D        2  2  7        1  q  s
    16        1  B  D        3  3  8        0  p  r
    17        1  B  D        3  3  8        1  q  s
    18        1  B  D        4  4  9        0  p  r
    19        1  B  D        4  4  9        1  q  s
    20        2  C  E        0  0  5        0  p  r
    21        2  C  E        0  0  5        1  q  s
    22        2  C  E        1  1  6        0  p  r
    23        2  C  E        1  1  6        1  q  s
    24        2  C  E        2  2  7        0  p  r
    25        2  C  E        2  2  7        1  q  s
    26        2  C  E        3  3  8        0  p  r
    27        2  C  E        3  3  8        1  q  s
    28        2  C  E        4  4  9        0  p  r
    29        2  C  E        4  4  9        1  q  s
    """
    dfs_index_name = [
        df.index.name if df.index.name else 'index' for df in dfs
    ]
    dfs = [
        df.reset_index().rename(
            columns={dfs_index_name[i]: dfs_index_name[i] + "_" + str(i)})
        if dfs_index_name[i] == 'index' else df.reset_index()
        for i, df in enumerate(dfs)
    ]
    join_key = list(pd.compat.product(*[df.index for df in dfs]))
    list_combine_df = []
    for i, df in enumerate(dfs):
        list_combine_df.append(
            dfs[i].iloc[[x[i] for x in join_key], :].reset_index())
    df_return = pd.concat(list_combine_df, axis=1, ignore_index=False)
    del df_return['index']
    return df_return

import pandas as pd
from sqlalchemy import create_engine, VARCHAR, NUMERIC
from datetime import datetime
from tidyframe import drop_table

engine = create_engine('sqlite:///testing_drop_table.db')
df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = 1
df['c'] = 1.3
df['d'] = [pd.np.nan, 10, 1.4]
df['e'] = ['adev', pd.NaT, '今天天氣']
df['f'] = [datetime.now(), None, datetime.now()]
df['g'] = [True, False, True]
df['h'] = 2147483647 * 2


def test_drop_table_basic():
    df.to_sql('raw_table', engine)
    drop_table('raw_table', engine)

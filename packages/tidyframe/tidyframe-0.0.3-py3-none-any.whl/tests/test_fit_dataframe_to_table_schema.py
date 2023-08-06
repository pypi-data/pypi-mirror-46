import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from datetime import datetime
from tidyframe import fit_table_schema_type

engine = create_engine('sqlite:///testing_fit_table_schema_type.db')
df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = 1
df['c'] = 1.3
df['d'] = [pd.np.nan, 10, 1.4]
df['e'] = ['adev', pd.NaT, '今天天氣']
df['f'] = [datetime.now(), None, datetime.now()]
df['g'] = [True, False, True]
df['h'] = 2147483647 * 2

df.to_sql('test_fit_dataframe', engine, index=False)
table = Table('test_fit_dataframe', MetaData(bind=engine), autoload=True)


def test_fit_table_schema_type_basic():
    df = pd.DataFrame()
    df['a'] = list('abc')
    df['b'] = 1
    df['c'] = 1.3
    df['d'] = [pd.np.nan, 10, 1.4]
    df['e'] = ['adev', pd.NaT, '今天天氣']
    df['f'] = pd.to_datetime(
        ['2018-03-09 22:29:00+08:00', '2018-03-09 22:29:00+08:00', None])
    df['g'] = [True, False, True]
    df['h'] = 2147483647 * 2
    fit_table_schema_type(df, table)
    df.to_sql('test_fit_dataframe', engine, index=False, if_exists='append')


def test_fit_table_schema_type_null():
    df = pd.DataFrame()
    df['a'] = list('abc')
    df['b'] = 1
    df['c'] = 1.3
    df['d'] = [pd.np.nan, 10, 1.4]
    df['e'] = ['adev', pd.NaT, '今天天氣']
    df['f'] = [None, None, None]
    df['g'] = [True, False, True]
    df['h'] = 2147483647 * 2
    fit_table_schema_type(df, table)
    df.to_sql('test_fit_dataframe', engine, index=False, if_exists='append')

import pandas as pd
from sqlalchemy import create_engine, VARCHAR, NUMERIC
from datetime import datetime
from tidyframe import create_table

engine = create_engine('sqlite:///testing_create_table.db')
df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = 1
df['c'] = 1.3
df['d'] = [pd.np.nan, 10, 1.4]
df['e'] = ['adev', pd.NaT, '今天天氣']
df['f'] = [datetime.now(), None, datetime.now()]
df['g'] = [True, False, True]
df['h'] = 2147483647 * 2


def test_create_table_basic():
    table_object = create_table(df,
                                'test_table',
                                engine,
                                primary_key=['a'],
                                nvarchar_columns=['e'],
                                non_nullable_columns=['d'],
                                create=False)


def test_create_table_basic2():
    table_object = create_table(df,
                                'test_table_create',
                                engine,
                                primary_key=['a'],
                                nvarchar_columns=['e'],
                                non_nullable_columns=['d'],
                                create=True)


def test_create_table_basic3():
    table_object = create_table(df,
                                'test_table_create2',
                                engine,
                                primary_key=['a'],
                                nvarchar_columns=['e'],
                                non_nullable_columns=['d'],
                                base_float_type=NUMERIC(3, 5),
                                create=True)

import pandas as pd
from sqlalchemy import (create_engine, VARCHAR, Column, DateTime)
from datetime import datetime
from tidyframe import copy_table_schema

engine = create_engine('sqlite:///testing_for_source_schema_sqlite.db')
engine_target = create_engine('sqlite:///testing_for_copy_schema_sqlite.db')
df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = 1
df['c'] = 1.3
df['d'] = [pd.np.nan, 10, 1.4]
df['e'] = ['adev', pd.NaT, '今天天氣']
df['f'] = [datetime.now(), None, datetime.now()]
df['g'] = [True, False, True]


def test_copy_table_schema():
    df.to_sql('raw_table', engine)
    copy_table_schema('raw_table',
                      'target_table',
                      source_con=engine,
                      target_con=engine_target,
                      add_columns=[Column('last_maintain_date', DateTime())],
                      omit_collation=True,
                      create=False)


def test_copy_table_schema_create():
    df.to_sql('raw_table_v2', engine)
    copy_table_schema('raw_table_v2',
                      'target2_table',
                      source_con=engine,
                      target_con=engine_target,
                      add_columns=[Column('last_maintain_date', DateTime())],
                      omit_collation=True,
                      create=True)

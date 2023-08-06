import pandas as pd
from sqlalchemy import create_engine, VARCHAR, NUMERIC
from datetime import datetime
from tidyframe import create_table, get_create_table_script

engine = create_engine('sqlite:///testing_get_create_table_script.db')
df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = 1
df['c'] = 1.3


def test_get_create_table_script_basic():
    table_object = create_table(df,
                                'test_table',
                                engine,
                                primary_key=['a'],
                                nvarchar_columns=['e'],
                                non_nullable_columns=['d'],
                                create=False)
    assert get_create_table_script(table_object)=='\nCREATE TABLE test_table (\n\ta CHAR(1) NOT NULL, \n\tb INTEGER, \n\tc FLOAT, \n\tPRIMARY KEY (a)\n)\n\n', 'get create table script not match'
    
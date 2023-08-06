import pandas as pd
from sqlalchemy import (create_engine, Table, MetaData)
from tidyframe import (load_table_schema, create_table)

engine = create_engine('sqlite:///load_table_schema.db')

num_row = 100000
df = pd.DataFrame()
df['a'] = ['a'] * num_row
df['b'] = ['b'] * num_row
df['c'] = ['c'] * num_row


def test_load_table_schema():
    create_table(df, 'test_table', engine, create=True)
    records = df.to_dict('record')
    table_b = load_table_schema('test_table', engine)

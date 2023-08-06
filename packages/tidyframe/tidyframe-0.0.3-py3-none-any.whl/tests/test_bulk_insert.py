import pandas as pd
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from datetime import datetime
from tidyframe import (create_table, load_table_schema, bulk_insert)
from funcy import chunks
from tidyframe import create_table

engine = create_engine('sqlite:///testing_bulk_insert.db')

num_row = 100000
df = pd.DataFrame()
df['a'] = ['a'] * num_row
df['b'] = ['b'] * num_row
df['c'] = ['c'] * num_row


def test_bulk_insert_basic():
    create_table(df, 'test_table', engine, create=True)
    records = df.to_dict('record')
    table_b = load_table_schema('test_table', engine)
    bulk_insert(records, table_b, engine)

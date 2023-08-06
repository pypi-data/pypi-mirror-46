import pandas as pd
from tidyframe import get_batch_dataframe

df = pd.DataFrame()
df['a'] = list('abc')
df['b'] = [1,2,3]

def test_get_batch_dataframe():
    get_batch_dataframe(df, 2)

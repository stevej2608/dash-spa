import pandas as pd

def user_db(database_uri) :
    df = pd.read_sql_table('user', database_uri)
    df = df.drop(['password'], axis=1)
    df.index = df['id']
    return df

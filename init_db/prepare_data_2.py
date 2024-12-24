from datetime import datetime
import pandas as pd
from clear_data import fill_missing_lat_lon

def formating_df(df):
    df = rename_columns(df)
    df = add_columns(df)
    df = change_the_date_format(df)
    return df

def rename_columns(df):
    df.rename(columns={
        'City': 'city',
        'Country': 'country_txt',
        'Perpetrator': 'gname',
        'Weapon': 'attacktype1_txt',
        'Injuries': 'nwound',
        'Fatalities': 'nkill',
        'Description': 'targtype1_txt'
    }, inplace=True)
    return df

def add_columns(df):
    df['nperps'] = 0
    df['region_txt'], df['latitude'], df['longitude'] = None, None, None
    df = fill_missing_lat_lon(df)
    return df

def change_the_date_format(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    df['iyear'] = df['Date'].apply(
        lambda x: 1900 + x.year % 100 if pd.notnull(x) and x.year > datetime.now().year else x.year
    )
    df['imonth'] = df['Date'].dt.month
    df['iday'] = df['Date'].dt.day
    df = df.drop(columns=['Date'])
    return df

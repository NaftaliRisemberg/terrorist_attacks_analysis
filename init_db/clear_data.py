import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import time
import os
from dotenv import load_env

API_KEY = os.getenv('CORRODES_API_KEY')
CORRODES_URL = os.getenv('CORRODES_URL')

def clear_all(df):
    df = clean_missing_dates(df)
    df = replace_missing_nperps(df)
    df = fill_missing_lat_lon(df)
    df = to_ints(df, 'nkill', 'nwound', 'nperps')
    return df

def clean_missing_dates(df):
    missing_dates = df[(df['imonth'] == 0) | (df['iday'] == 0)].index
    drop_missing_dates = df.drop(missing_dates, inplace=False)
    return drop_missing_dates

def replace_missing_nperps(df):
    df['nperps'] = df['nperps'].map({-99: 0})
    df['nperps'] = df['nperps'].infer_objects()

    return df

def get_lat_and_long_by_location(df):
    is_city =  df['city'] != "Unknown"
    if is_city:
        city = df['city'].iloc[0]
        lat, lon = get_lat_long(city, city)
    else:
        country = df['country_txt'].iloc[0]
        lat, lon = get_lat_long(country, country)
    return lat, lon

def get_lat_long(location_type, location_name):
    try:
        url = f"{CORRODES_URL}{location_type}={location_name}&apiKey={API_KEY}"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers).json()

        for feature in resp['features']:
            lat, lon = feature['geometry']['coordinates']
            return lat, lon
        return None, None

    except Exception as e:
        print(f"Error message: {e}")

def fill_missing_lat_lon(df):
    max_calls_per_minute = 100
    calls_counter = 0
    sleep_time = 60

    for index, row in df.iterrows():
        if pd.isnull(row['latitude']) or pd.isnull(row['longitude']):
            if pd.notnull(row['city']) and row['city'] != "Unknown":
                city = row['city']
                lat, lon = get_lat_long('city', city)
                df.at[index, 'latitude'] = lat
                df.at[index, 'longitude'] = lon

            elif pd.notnull(row['country_txt']):
                country = row['country_txt']
                lat, lon = get_lat_long('country', country)
                df.at[index, 'latitude'] = lat
                df.at[index, 'longitude'] = lon

            else:
                print(f"Missing both city and country for row {index}")

        if calls_counter >= max_calls_per_minute:
            print(f"API limit reached, sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
            calls_counter = 0
    return df

def to_ints(df, *fields):
    for field in fields:
        if field in df.columns:
            df[field] = df[field].fillna(0).astype(int)
        else:
            print(f"{field} not found in DataFrame")
    return df


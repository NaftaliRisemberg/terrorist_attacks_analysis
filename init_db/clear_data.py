import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

api_key ='629deed504ed401c977d8dba2ae06386'
corrodes_api = 'https://api.geoapify.com/v1/geocode/search?'

def clear_all(df):
    df = clean_missing_dates(df)
    df = replace_missing_nperprs(df)
    df = fill_missing_lat_lon(df)
    return df

def clean_missing_dates(df):
    drop_missing_dates = df[(df['imonth'] == 0) | (df['iday'] == 0)].index
    drop_missing_dates = df.drop(drop_missing_dates, inplace=False)
    print("ףףףף")
    return drop_missing_dates


def replace_missing_nperprs(df):
    df['nperps'] = df['nperps'].map({-99: 0})
    df['nperps'] = df['nperps'].infer_objects()
    df['nperps'] = df['nperps'].fillna(df['nperps'])

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
        url = f"{corrodes_api}{location_type}={location_name}&apiKey={api_key}"

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
    return df


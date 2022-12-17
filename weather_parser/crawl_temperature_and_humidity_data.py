#!/usr/bin/env python3
import os
from calendar import monthrange
from time import sleep
from pickle import dump, load

import requests
import pandas as pd

from settings.settings import HISTORIC_DATA_FOLDER, WEATHER_DATA_URL, WEATHER_LOCATION_ID, WEATHER_LOCATION_NAME

FR_MONTH = {
    1: 'janvier',
    2: 'fevrier',
    3: 'mars',
    4: 'avril',
    5: 'mai',
    6: 'juin',
    7: 'juillet',
    8: 'aout',
    9: 'septembre',
    10: 'octobre',
    11: 'novembre',
    12: 'decembre',
}


def parse_weather_raw_html_page(raw, year, month, day):
    def _get_columns_to_drop():
        delta = set(expected_columns) - set(df.columns)
        return set(expected_columns) - delta

    expected_columns = ['Temps', 'Pluie', 'Vent', 'Pt. de rosée',
                        'Pression', 'Température', 'Humidité', 'Heure locale', 'Bio-météo']
    dfs = pd.read_html(raw, header=0)
    assert 3 == len(dfs), 'Wrong data model in parsed temperature data. Possibly a date in the future.'
    df = dfs[1]
    del dfs

    columns_to_drop = _get_columns_to_drop()
    df['Temp'] = df['Température'].str.replace(' °C', '')
    df['Temp'] = pd.to_numeric(df['Temp'])
    df['PctHumid'] = df['Humidité'].str.replace('%', '')
    df['PctHumid'] = pd.to_numeric(df['PctHumid'])

    dt_format = '%Hh'
    try:
        df['dt'] = pd.to_datetime(df['Heure locale'], format=dt_format)
    except KeyError:
        df['dt'] = pd.to_datetime(df['Heure locale  access_time  30mn METAR'], format=dt_format)
    df['dt'] = df['dt'].map(lambda t: t.replace(year=year, month=month, day=day))
    df.set_index('dt', inplace=True)

    df.drop(columns=columns_to_drop, inplace=True)

    return df


def _crawl_month(year, month):
    month_dict = dict()
    number_of_days_in_month = monthrange(year, month)[1]
    for day in range(1, number_of_days_in_month + 1):
        print('====', year, month, day)
        pickle_day_name = f'climate_{year}-{month:02}-{day:02}.pickle'

        if not os.path.exists(os.path.join(HISTORIC_DATA_FOLDER, pickle_day_name)):
            df = download_weather_data_of_day(year, month, day)
            with open(os.path.join(HISTORIC_DATA_FOLDER, pickle_day_name), 'wb') as fh:
                dump(df, fh)
            sleep(2)
        else:  # pickled
            with open(os.path.join(HISTORIC_DATA_FOLDER, pickle_day_name), 'rb') as fh:
                df = load(fh)
        month_dict[day] = df

    return month_dict


def download_weather_data_of_day(year, month, day):
    if 1 == day:
        day_as_url = '1er'
    else:
        day_as_url = str(day)

    url = f'{WEATHER_DATA_URL}{day_as_url}/{FR_MONTH[month]}/{year}/{WEATHER_LOCATION_NAME}/{WEATHER_LOCATION_ID}'
    print('url:', url)
    try:
        response = requests.get(url)
        assert 200 == response.status_code
        print('query successful!')
    except AssertionError:
        return None

    return parse_weather_raw_html_page(response.text, year, month, day)


if __name__ == '__main__':
    all_weather = dict()
    for year in [2021, 2022]:
        all_weather[year] = dict()
        for month in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
            pickled_month_file_name = f'climate_month_{year}-{month:02}.pickle'
            if os.path.exists(os.path.join(HISTORIC_DATA_FOLDER, pickled_month_file_name)):
                print(f'Already downloaded: {year}-{month:02}')
                with open(os.path.join(HISTORIC_DATA_FOLDER, pickled_month_file_name), 'rb') as fh:
                    current_month = load(fh)
            else:
                current_month = _crawl_month(year, month)

                with open(os.path.join(HISTORIC_DATA_FOLDER, pickled_month_file_name), 'wb') as fh:
                    dump(current_month, fh)

            all_weather[year][month] = current_month

    # df = download_weather_data_of_day(2022, 12, 21)
    # print(df)

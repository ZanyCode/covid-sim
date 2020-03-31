import pipetools
import requests
import streamlit as st
from pipetools import pipe, as_args
import pandas as pd
import numpy as np

from common import URL_CASES_TIME, URL_CASES, URL_CASES_TIME_US, Cols


@st.cache(hash_funcs={pipetools.main.Pipe: lambda x: x})
def get_data():
    return URL_CASES_TIME > \
          (pipe
           # Download timeseries
           | download_json
           | to_dataframe
           # Download most recent cases
           | add_track(download_json, URL_CASES)
           | for_track(to_dataframe, track_idx=1)
           # Download timeseries for US
           | add_track(download_json, URL_CASES_TIME_US)
           | for_track(to_dataframe, track_idx=2)
           # Join everything together
           | as_args(join_dfs)
           | remove_invalid_countries
           | convert_last_update_to_datetime
           | sort)


def download_json(url):
    return requests.get(url).json()


def to_dataframe(case_time_json):
    extracted_columns = [entry["attributes"] for entry in case_time_json["features"]]
    return pd.DataFrame(extracted_columns)


def join_dfs(cases_time, cases, cases_time_us):
    return cases_time.append(cases, ignore_index=True).append(cases_time_us, ignore_index=True)


def convert_last_update_to_datetime(df):
    return df.assign(Last_Update=df[Cols.LastUpdate].apply(lambda n: pd.Timestamp(n, unit="ms")))


def remove_invalid_countries(df):
    df_by_country = df.groupby(Cols.Country)[Cols.Country]
    valid_country_mask = df_by_country.count().to_numpy() > 1
    valid_countries = np.array(list(df_by_country.groups.keys()))[valid_country_mask]
    return df[df[Cols.Country].isin(valid_countries)]


def sort(df):
    return df.sort_values([Cols.Country, Cols.LastUpdate])


def add_track(function, *args):
    return lambda x: [x, function(*args)] if type(x) is not list else x + [function(*args)]


def for_track(function, track_idx=0):
    return lambda tracks: [track if idx != track_idx else function(track) for idx, track in enumerate(tracks)]

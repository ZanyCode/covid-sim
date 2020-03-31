import pandas as pd
from typing import Callable, NamedTuple

from common import Cols

infection_rate = 3.0
days_infection_to_death = 14
case_fatality_percent = 2.5


class Feature(NamedTuple):
    name: str
    generate: Callable[[pd.DataFrame], pd.DataFrame]


def get_available_features():
    return [
        Feature(Cols.Confirmed, generate_feature_confirmed),
        Feature(Cols.Deaths, generate_feature_deaths),
        Feature("Simulated Infections", generate_simulated_infections)
    ]


def generate_feature_confirmed(df: pd.DataFrame, name: str):
    extracted_cols = df[[Cols.LastUpdate, Cols.Country, Cols.Confirmed]]
    extracted_cols.columns = list(extracted_cols.columns)[:-1] + [Cols.Data]
    return add_feature_col(extracted_cols, name)


def generate_feature_deaths(df: pd.DataFrame, name: str):
    extracted_cols = df[[Cols.LastUpdate, Cols.Country, Cols.Deaths]]
    extracted_cols.columns = list(extracted_cols.columns)[:-1] + [Cols.Data]
    return add_feature_col(extracted_cols, name)


def generate_simulated_infections(df: pd.DataFrame, name: str):
    doubling_intervals = days_infection_to_death / infection_rate
    new_deaths = df[Cols.Deaths][df[Cols.Deaths] > 0].diff().fillna(0.0)
    new_infections = new_deaths.apply(lambda x: x / (case_fatality_percent / 100) * pow(2, doubling_intervals))
    simulated_infections = new_infections.cumsum()
    df_feature = df[[Cols.LastUpdate, Cols.Country]]
    df_feature = df_feature.assign(**{Cols.Data: simulated_infections})
    return add_feature_col(df_feature, name)


def add_feature_col(df: pd.DataFrame, feature_name: str):
    return df.assign(**{Cols.Feature: feature_name})

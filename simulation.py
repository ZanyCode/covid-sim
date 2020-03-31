import pandas as pd
from typing import Callable, NamedTuple

from common import Cols

infection_rate = 6.0
days_infection_to_death = 10
case_fatality_percent = 3.0


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
    simulated_infections = df[Cols.Deaths][df[Cols.Deaths] > 0].apply(lambda x: x / (case_fatality_percent / 100))
    shifted_date = df[Cols.LastUpdate].apply(lambda x: x - pd.Timedelta(days=days_infection_to_death))

    df_feature = df[[Cols.LastUpdate, Cols.Country]]
    df_feature = df_feature.assign(**{Cols.Data: simulated_infections, Cols.LastUpdate: shifted_date})

    doubling_intervals = days_infection_to_death / infection_rate
    last_by_country = df.groupby(Cols.Country).last().reset_index(level=0)
    extrapolated_infections = last_by_country[Cols.Deaths].apply(lambda x: x / (case_fatality_percent / 100) * pow(2, doubling_intervals))
    last_by_country = last_by_country.assign(**{Cols.Data: extrapolated_infections})
    last_by_country = last_by_country[[Cols.LastUpdate, Cols.Country, Cols.Data]]

    combined_df = df_feature.append(last_by_country, ignore_index=True).sort_values([Cols.Country, Cols.LastUpdate])

    return add_feature_col(combined_df, name)


def add_feature_col(df: pd.DataFrame, feature_name: str):
    return df.assign(**{Cols.Feature: feature_name})

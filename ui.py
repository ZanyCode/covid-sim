import sys
from typing import List, Callable, Any, NamedTuple

from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.express as px

import simulation
from common import Cols
from data import get_data
from simulation import get_available_features, Feature, generate_simulated_infections

this = sys.modules[__name__]
use_log_scale = False


def run():
    df: DataFrame = get_data()
    generate_simulated_infections(df, "")
    features = get_available_features()

    selected_view = st.sidebar.selectbox("View", get_views(), format_func=lambda view: view.name)
    view_simulation_settings()
    selected_view.show(df, features)


def view_countries_by_feature(df: pd.DataFrame, features: List[Feature]):
    selected_feature = st.selectbox("Feature", features, format_func=lambda f: f.name)
    df_features_all = selected_feature.generate(df, selected_feature.name)
    selected_countries = st.multiselect("Countries", df_features_all[Cols.Country].unique())

    if len(selected_countries) > 0:
        df_features_country = df_features_all[df_features_all[Cols.Country].isin(selected_countries)]
        fig = px.scatter(df_features_country, x=Cols.LastUpdate, y=Cols.Data, color=Cols.Country)
        yaxis_type = "log" if this.use_log_scale else "linear"
        fig.update_layout(title="Countries by Feature", yaxis_title=selected_feature.name, xaxis_title="Time", yaxis_type=yaxis_type)
        # fig.update_layout(title="Countries by Feature", yaxis_title=selected_feature.name, xaxis_title="Time")
        st.plotly_chart(fig)


def view_features_by_country(df: pd.DataFrame, features: List[Feature]):
    selected_features = st.multiselect("Features", features, features[0], format_func=lambda f: f.name)
    if len(selected_features) > 0:
        df_features_all = pd.concat([f.generate(df, f.name) for f in selected_features])
        selected_country = st.selectbox("For Country", df_features_all[Cols.Country].unique())
        df_features_country = df_features_all[df_features_all[Cols.Country] == selected_country]

        fig = px.scatter(df_features_country, x=Cols.LastUpdate, y=Cols.Data, color=Cols.Feature)
        yaxis_type = "log" if this.use_log_scale else "linear"
        fig.update_layout(title="Features by Country", yaxis_title="Value", xaxis_title="Time", yaxis_type=yaxis_type)
        st.plotly_chart(fig)


def view_simulation_settings():
    simulation.case_fatality_percent = \
        st.sidebar.number_input("Case Fatality (%)", min_value=0.0, max_value=100.0, value=simulation.case_fatality_percent, key='casefatality')
    simulation.days_infection_to_death = \
        st.sidebar.number_input("Days between Infection and Death", min_value=1, max_value=100, value=simulation.days_infection_to_death, key='ttd')
    simulation.infection_rate = \
        st.sidebar.number_input("Infection Rate (Days to Double Infections)", min_value=0.5, max_value=100.0, value=simulation.infection_rate, key='ir')
    this.use_log_scale = st.sidebar.checkbox("Use Log Scaling", use_log_scale)


class View(NamedTuple):
    name: str
    show: Callable[[pd.DataFrame, List[Feature]], Any]


def get_views():
    return [
        View("Compare Features for Country", view_features_by_country),
        View("Compare Countries for Feature", view_countries_by_feature)
    ]


if __name__ == "__main__":
    run()

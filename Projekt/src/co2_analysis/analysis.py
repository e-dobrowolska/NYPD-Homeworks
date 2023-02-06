import pandas as pd
import numpy as np


def merge_data(api_gdp, api_pop, co2):
    pop_melt = pd.melt(api_pop, id_vars="Country Name", value_vars=api_pop.columns[4:])
    pop_melt.columns = ["Country", "Year", "Population"]

    gdp_melt = pd.melt(api_gdp, id_vars="Country Name", value_vars=api_gdp.columns[4:])
    gdp_melt.columns = ["Country", "Year", "GDP"]

    pop_gdp = pop_melt.merge(gdp_melt, on=["Country", "Year"])
    pop_gdp["Year"] = pop_gdp["Year"].astype("int64")

    pop_gdp_co2 = pop_gdp.merge(co2, on=["Country", "Year"])
    return pop_gdp_co2


def co2_ranking(merged_data):
    ranking = merged_data.sort_values(['Year', 'Per Capita'], ascending=[True, False]).groupby('Year').head(5)
    return ranking[["Year", "Country", "Total", "Per Capita"]]


def gdp_ranking(merged_data):
    merged_data["GDP Per Capita"] = merged_data["GDP"]/merged_data["Population"]
    ranking = merged_data.sort_values(['Year', 'GDP Per Capita'], ascending=[True, False]).groupby('Year').head(5)
    return ranking[["Year", "Country", "GDP", "GDP Per Capita"]]


def co2_reduction_ranking(merged_data, start_year, end_year):
    pivot_df = merged_data.pivot(index='Country', columns='Year')['Per Capita']
    pivot_df["Reduction"] = pivot_df[end_year]-pivot_df[start_year]
    pivot_df = pivot_df["Reduction"].sort_values()
    pivot_df = pivot_df.dropna()
    return pivot_df.head(5), pivot_df.tail(5).sort_values(ascending=False)

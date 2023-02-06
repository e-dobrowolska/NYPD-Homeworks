import pandas as pd
import numpy as np


def co2_ranking(merged_data):
    """
    Creates a ranking of countries and their CO2 emission (top 5 countries in each year)
    :param merged_data: a DataFrame with Countries, years, CO2 emissions, CO2 emission Per Capita (obtained
    using merge_data() function on DataFrames: api_pop (countries, years, population), api_gdp (countries, years, GDP),
    co2 (countries, years, CO2)
    :return: a DataFrame with 5 countries with the highest CO2 emission and CO2 Per Capita emission in each year
    """
    ranking = merged_data.sort_values(['Year', 'Per Capita'], ascending=[True, False]).groupby('Year').head(5)
    return ranking[["Year", "Country", "Total", "Per Capita"]]


def gdp_ranking(merged_data):
    """
    Creates a ranking of countries and their GDP (top 5 countries in each year)
    :param merged_data: a DataFrame with countries, years, GDP (obtained using merge_data() function on DataFrames:
    api_pop (countries, years, population), api_gdp (countries, years, GDP), co2 (countries, years, CO2)
    :return: a DataFrame with 5 countries with the highest GDP and GDP Per Capita in each year
    """
    merged_data["GDP Per Capita"] = merged_data["GDP"]/merged_data["Population"]
    ranking = merged_data.sort_values(['Year', 'GDP Per Capita'], ascending=[True, False]).groupby('Year').head(5)
    return ranking[["Year", "Country", "GDP", "GDP Per Capita"]]


def co2_reduction_ranking(merged_data, end_year, number_of_years=10):
    """
    Creates a ranking of countries regarding their CO2 emission reduction
    :param merged_data: a DataFrame with countries, years, GDP (obtained using merge_data() function on DataFrames:
    api_pop (countries, years, population), api_gdp (countries, years, GDP), co2 (countries, years, CO2)
    :param end_year:
    :param number_of_years: 
    :return: A table with 5 countries that within the specified time range reduced their CO2 emission the most, and a
    second table with 5 countries that increased their CO2 emission the most.
    """
    pivot_df = merged_data.pivot(index='Country', columns='Year')['Per Capita']
    pivot_df["Reduction"] = pivot_df[end_year]-pivot_df[end_year-number_of_years]
    pivot_df = pivot_df["Reduction"].sort_values()
    pivot_df = pivot_df.dropna()
    return pivot_df.head(5), pivot_df.tail(5).sort_values(ascending=False)

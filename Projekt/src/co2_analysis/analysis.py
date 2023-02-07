import pandas as pd
import numpy as np
import warnings


def co2_ranking(merged_data, start_year=None, end_year=None):
    """
    Creates a ranking of countries and their per capita CO2 emission (top 5 countries in each year)
    :param merged_data: a DataFrame with Countries, years, CO2 emission, CO2 emission Per Capita (obtained
    using merge_data() function on DataFrames: api_pop (countries, years, population), api_gdp (countries, years, GDP),
    co2 (countries, years, CO2))
    :param start_year: year, from which the ranking should begin
    :param end_year: year, on which the ranking should end
    :return: a DataFrame with 5 countries with the highest CO2 Per Capita emission in each year along with their CO2
    Per Capita emission and their total CO2 emission.
    """

    # If the user didn't provide parameters start_year or end_year, they are set to 0 and max(Year), respectively
    start_year = 0 if start_year is None else start_year
    end_year = max(merged_data["Year"]) if end_year is None else end_year

    if start_year <= end_year:  # check if the time range is non-empty
        ranking = merged_data.sort_values(['Year', 'Per Capita'], ascending=[True, False]).groupby('Year').head(5)
        return ranking[["Year", "Country", "Total", "Per Capita"]][(ranking["Year"] >= start_year) & (ranking["Year"] <= end_year)]
    else:
        warnings.warn(r"Start Year can't be after End Year. Defaulting to range: all years")
        return co2_ranking(merged_data)


def gdp_ranking(merged_data, start_year=None, end_year=None):
    """
    Creates a ranking of countries and their per capita GDP (top 5 countries in each year)
    :param merged_data: a DataFrame with countries, years, GDP (obtained using merge_data() function on DataFrames:
    api_pop (countries, years, population), api_gdp (countries, years, GDP), co2 (countries, years, CO2))
    :param start_year: year, from which the ranking should begin
    :param end_year: year, on which the ranking should end
    :return: a DataFrame with 5 countries with the highest GDP Per Capita emission in each year along with their GDP
    Per Capita and their GDP.
    """

    # If the user didn't provide parameters start_year or end_year, they are set to 0 and max(Year), respectively
    start_year = 0 if start_year is None else start_year
    end_year = max(merged_data["Year"]) if end_year is None else end_year

    if start_year <= end_year:  # check if the time range is non-empty
        merged_data["GDP Per Capita"] = merged_data["GDP"]/merged_data["Population"]
        ranking = merged_data.sort_values(['Year', 'GDP Per Capita'], ascending=[True, False]).groupby('Year').head(5)
        return ranking[["Year", "Country", "GDP", "GDP Per Capita"]][(ranking["Year"] >= start_year) & (ranking["Year"] <= end_year)]
    else:
        warnings.warn(r"Start Year can't be after End Year. Defaulting to range: all years")
        return gdp_ranking(merged_data)


def co2_reduction_ranking(merged_data, up_to_year=None, number_of_years=10):
    """
    Creates rankings of countries regarding their CO2 emission changes: the greatest reduction and the greatest increase
    :param merged_data: a DataFrame with countries, years, GDP (obtained using merge_data() function on DataFrames:
    api_pop (countries, years, population), api_gdp (countries, years, GDP), co2 (countries, years, CO2))
    :param up_to_year: End Year of the analysis
    :param number_of_years: Number of analysed years. Start year of the analysis will be calculated as
    up_to_year-number_of_years.
    :return: A table with 5 countries that within the specified time range reduced their CO2 emission the most, and a
    second table with 5 countries that increased their CO2 emission the most.
    """

    # if the user didn't provide the parameter up_to_year, it is set to the maximum year in the data
    up_to_year = max(merged_data["Year"]) if up_to_year is None else up_to_year

    # if the user provided the years that don't exist in the data, return the call with default parameters
    if up_to_year not in merged_data["Year"].unique() or up_to_year-number_of_years not in merged_data["Year"].unique():
        warnings.warn('Years you are interested in don\'t exist. Returning the call with default parameters.')
        return co2_reduction_ranking(merged_data)

    pivot_df = merged_data.pivot(index='Country', columns='Year')['Per Capita']
    pivot_df["Reduction"] = pivot_df[up_to_year]-pivot_df[up_to_year-number_of_years]  # calculate reduction
    pivot_df = pivot_df["Reduction"].sort_values()
    pivot_df = pivot_df.dropna()
    return pd.DataFrame(pivot_df.head(5)), pd.DataFrame(pivot_df.tail(5).sort_values(ascending=False))

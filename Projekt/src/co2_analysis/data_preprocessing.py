import pandas as pd
import numpy as np
import warnings


def correct_api(api_data):
    """
    Corrects an api DataFrame (previously read as one column). Splits it into multiple columns, changes columns' types
    into numeric, sets header.
    :param api_data: a DataFrame (api_pop or api_gdp)
    :return: a corrected api DataFrame
    """
    api_data = api_data.iloc[:, 0].str.split(',"', expand=True)  # split into multiple columns
    api_data = api_data.applymap(lambda x: x.strip('",'))  # remove quotation marks and commas
    api_data.columns = api_data.iloc[0]  # set the first row as column names
    api_data = api_data[1:]  # remove the first row
    api_data.reset_index(drop=True, inplace=True)
    api_data.replace('', np.nan, inplace=True)  # encode NaN
    for col in api_data.columns[4:]:
        api_data[col] = api_data[col].astype('float')  # change types

    return api_data


def merge_data(api_gdp, api_pop, co2):
    """
    The function merges three dataframes into one.
    :param api_gdp: DataFrame with countries and their GDP
    :param api_pop: DataFrame with countries and their population
    :param co2: DataFrame with countries and their CO2 emission
    :return: a dataframe with countries, their population, GDP, and CO2 emission over the years
    """
    pop_melt = pd.melt(api_pop, id_vars="Country Name", value_vars=api_pop.columns[4:])
    pop_melt.columns = ["Country", "Year", "Population"]
    pop_melt["Country"] = pop_melt["Country"].map(lambda x: x.upper())  # uppercase Country Names (to match other data)

    gdp_melt = pd.melt(api_gdp, id_vars="Country Name", value_vars=api_gdp.columns[4:])
    gdp_melt.columns = ["Country", "Year", "GDP"]
    gdp_melt["Country"] = gdp_melt["Country"].map(lambda x: x.upper())  # uppercase Country Names (to match other data)

    # Sets of Countries appearing in pop_melt, gdp_melt, co2
    pop_countries = set(pop_melt["Country"].unique())
    gdp_countries = set(gdp_melt["Country"].unique())
    co2_countries = set(co2["Country"].unique())

    # symmetric difference between three sets
    diff = (pop_countries | gdp_countries | co2_countries) - (pop_countries & gdp_countries & co2_countries)

    if diff:  # inform the user that some countries don't appear in all datasets
        warnings.warn(f"{len(diff)} countries/regions don\'t appear in all datasets and have been excluded from the study.")

    pop_gdp = pop_melt.merge(gdp_melt, on=["Country", "Year"])  # merge
    pop_gdp["Year"] = pop_gdp["Year"].astype("int64")

    pop_gdp_co2 = pop_gdp.merge(co2, on=["Country", "Year"])  # merge

    return pop_gdp_co2

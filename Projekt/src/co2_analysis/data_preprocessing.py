import pandas as pd
import numpy as np


def load_all_files(api_pop_path, api_gdp_path, co2_path):
    """
    The function loads all files into pandas DataFrames
    :param api_pop_path: path to the api file regarding countries and their populations
    :param api_gdp_path: path to the api file regarding countries and their GDP
    :param co2_path: path to the file regarding countries and their CO2 emission over the years
    :return: three pandas DataFrames: api_pop (read as one column), api_gdp (read as one column), and co2 (many columns).
    """
    api_pop = pd.read_csv(api_pop_path, sep="^", header=None, skiprows=4)  # read as one column
    api_gdp = pd.read_csv(api_gdp_path, sep="^", header=None, skiprows=4)  # read as one column
    co2 = pd.read_csv(co2_path)

    return api_pop, api_gdp, co2


def correct_api(api_data):
    """
    Corrects an api DataFrame (previously read as one column). Splits it into multiple columns, changes columns' types
    into numeric, sets header.
    :param api_data: a DataFrame, api_pop or api_gdp
    :return: a corrected api DataFrame
    """
    api_data = api_data.iloc[:, 0].str.split(',"', expand=True)
    api_data = api_data.applymap(lambda x: x.strip('",'))
    api_data.columns = api_data.iloc[0]
    api_data = api_data[1:]
    api_data.reset_index(drop=True, inplace=True)
    api_data.replace('', np.nan, inplace=True)
    for col in api_data.columns[4:]:
        api_data[col] = api_data[col].astype('float')

    return api_data


def clear_data(api_pop, api_gdp):
    """

    :param api_pop: a dataframe with countries and their populations
    :param api_gdp: a dataframe with countries and their GDP
    :return: DataFrames corrected with correct_api() function
    """
    api_pop = correct_api(api_pop)
    api_gdp = correct_api(api_gdp)

    return api_pop, api_gdp


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

    gdp_melt = pd.melt(api_gdp, id_vars="Country Name", value_vars=api_gdp.columns[4:])
    gdp_melt.columns = ["Country", "Year", "GDP"]

    pop_gdp = pop_melt.merge(gdp_melt, on=["Country", "Year"])
    pop_gdp["Year"] = pop_gdp["Year"].astype("int64")
    pop_gdp["Country"] = pop_gdp["Country"].map(lambda x: x.upper())

    pop_gdp_co2 = pop_gdp.merge(co2, on=["Country", "Year"])
    return pop_gdp_co2

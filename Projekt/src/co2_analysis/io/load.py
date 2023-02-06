import pandas as pd
import numpy as np


def load_pop(api_pop_path):
    with open(api_pop_path, 'r', newline='\n') as file:
        line = file.readline()

        df = []
        countries = []

        while line:
            row = []
            ctry_name = str()
            for value in line.split(","):
                if '""' in value:
                    row.append(value.strip('""'))
                else:
                    ctry_name += value

            df.append(row)
            countries.append(ctry_name)
            line = file.readline()

    api_pop = pd.DataFrame(df[1:])
    api_pop = api_pop.drop(api_pop.columns[2], axis=1)
    api_pop.columns = df[0]
    api_pop.replace('', np.nan, inplace=True)

    for col in api_pop.columns[3:]:
        api_pop[col] = api_pop[col].astype('float')

    api_pop.insert(0, "Country Name", [ctry.strip('\r\n"').upper() for ctry in countries[1:]])
    return api_pop


def load_gdp(api_gdp_path):
    with open(api_gdp_path, 'r', newline='\n') as file:
        line = file.readline()

        df = []
        countries = []

        while line:
            row = []
            ctry_name = str()
            for value in line.split(","):
                if '""' in value:
                    row.append(value.strip('""'))
                else:
                    ctry_name += value

            df.append(row)
            countries.append(ctry_name)
            line = file.readline()

    api_gdp = pd.DataFrame(df[1:])
    api_gdp.columns = df[0]
    api_gdp.replace('', np.nan, inplace=True)

    for col in api_gdp.columns[3:]:
        api_gdp[col] = api_gdp[col].astype('float')

    api_gdp.insert(0, "Country Name", [ctry.strip('\r\n"').upper() for ctry in countries[1:]])
    return api_gdp

def load_all_files(api_pop_path, api_gdp_path, co2_path):
    api_pop = load_pop(api_pop_path)
    api_gdp = load_gdp(api_gdp_path)
    co2 = pd.read_csv(co2_path)
    return api_pop, api_gdp, co2




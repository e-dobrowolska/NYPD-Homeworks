import pytest
import pandas as pd
import numpy as np
from src.co2_analysis import correct_api, merge_data, co2_ranking, gdp_ranking, co2_reduction_ranking


@pytest.fixture()
def dummy_api1():
    """
    :return: an api-like DataFrame (as one column)
    """
    header = 'Country Name,"Country Code","Indicator Name","Indicator Code","2001",'
    string1 = 'Hogwarts,"HG","magic","ma","",'
    string2 = 'Mimuw,"MIM","magic","ma","123",'
    string3 = 'Skyhold,"DA","magic","ma","0",'
    return pd.DataFrame([header, string1, string2, string3])


@pytest.fixture()
def dummy_co2():
    """
    :return: a co2-like DataFrame
    """
    df = pd.DataFrame({'Year': list(range(2000, 2006)),
                       'Country': ['MIMUW']*6,
                       'Total': [12, 321, 23123, 43342, 1232312, 212122],
                       'Per Capita': [0.1, 0.32, 0.213, 0.1232, 0.2332, 0.234]})
    return df


@pytest.fixture()
def dummy_merged():
    """
    :return: a DataFrame in the format returned by the function merge_data()
    """
    data_dict = {'Year': [2000 + i // 6 for i in range(36)],
                 'Country': ['Mimuw', 'Hogwarts', 'Skyhold', 'Quito', 'Hawaii', 'Warsaw'] * 6,
                 'Population': [np.random.uniform(100000, 500000) for x in range(36)],
                 'GDP': [np.random.uniform(1000000, 5000000) for x in range(36)],
                 'Total': [np.random.uniform(10000, 50000) for x in range(36)],
                 'Per Capita': [np.random.uniform(200, 1000) for x in range(36)]
                 }
    return pd.DataFrame(data_dict)


@pytest.fixture()
def corrected_api1():
    """
    :return: an api-like DataFrame (in corrected form)
    """
    api_dict = {'Country Name': ['Hogwarts', 'Mimuw', 'Skyhold'],
                "Country Code": ['HG', 'MIM', 'DA'],
                "Indicator Name": ['magic', 'magic', 'magic'],
                "Indicator Code": ['ma', 'ma', 'ma'],
                "2001": [np.nan, 123, 0]
                }
    return pd.DataFrame(api_dict)


@pytest.fixture()
def corrected_api2():
    """
    :return: an api-like DataFrame (in corrected form)
    """
    api_dict = {'Country Name': ['Quito', 'Mimuw', 'Skyhold'],
                "Country Code": ['EC', 'MIM', 'DA'],
                "Indicator Name": ['python', 'python', 'python'],
                "Indicator Code": ['py', 'py', 'py'],
                "2001": [np.nan, 123213, 312340]}
    return pd.DataFrame(api_dict)


# Test function correct_api()
def test_correct_api_shape(dummy_api1):
    corrected_api = correct_api(dummy_api1)
    assert corrected_api.shape == (3, 5)


def test_correct_api_columns(dummy_api1):
    corrected_api = correct_api(dummy_api1)
    assert np.all(corrected_api.columns == ["Country Name", "Country Code", "Indicator Name", "Indicator Code", "2001"])


def test_correct_api_nan(dummy_api1):
    corrected_api = correct_api(dummy_api1)
    assert np.isnan(corrected_api.iloc[0][4])


def test_correct_api_types(dummy_api1):
    corrected_api = correct_api(dummy_api1)
    assert corrected_api['2001'].dtypes == 'float64'


# Test function merge_data()
def test_merge_data_shape(corrected_api1, corrected_api2, dummy_co2):
    data_merged = merge_data(corrected_api1, corrected_api2, dummy_co2)
    assert data_merged.shape == (1, 6)


def test_merge_data_columns(corrected_api1, corrected_api2, dummy_co2):
    data_merged = merge_data(corrected_api1, corrected_api2, dummy_co2)
    assert np.all(data_merged.columns == ['Country', 'Year', 'Population', 'GDP', 'Total', 'Per Capita'])


# Test function co2_ranking()
def test_co2_ranking_monotonic_time(dummy_merged):
    big_ranking = co2_ranking(dummy_merged)
    small_ranking = co2_ranking(dummy_merged, 2003, 2004)
    assert big_ranking['Year'].is_monotonic
    assert small_ranking['Year'].is_monotonic


def test_co2_ranking_decreasing_co2_in_groups(dummy_merged):
    big_ranking = co2_ranking(dummy_merged)
    small_ranking = co2_ranking(dummy_merged, 2003, 2004)
    assert np.all(big_ranking['Per Capita'].groupby(big_ranking['Year']).is_monotonic_decreasing)
    assert np.all(small_ranking['Per Capita'].groupby(small_ranking['Year']).is_monotonic_decreasing)


def test_co2_ranking_results_within_time_range(dummy_merged):
    small_ranking = co2_ranking(dummy_merged, 2003, 2004)
    assert min(small_ranking['Year']) == 2003
    assert max(small_ranking['Year']) == 2004


# Test function gdp_ranking()
def test_gdp_ranking_monotonic_time(dummy_merged):
    big_ranking = gdp_ranking(dummy_merged)
    small_ranking = gdp_ranking(dummy_merged, 2003, 2004)
    assert big_ranking['Year'].is_monotonic
    assert small_ranking['Year'].is_monotonic


def test_gdp_ranking_decreasing_co2_in_groups(dummy_merged):
    big_ranking = gdp_ranking(dummy_merged)
    small_ranking = gdp_ranking(dummy_merged, 2003, 2004)
    assert np.all(big_ranking['GDP Per Capita'].groupby(big_ranking['Year']).is_monotonic_decreasing)
    assert np.all(small_ranking['GDP Per Capita'].groupby(small_ranking['Year']).is_monotonic_decreasing)


def test_gdp_ranking_results_within_time_range(dummy_merged):
    small_ranking = gdp_ranking(dummy_merged, 2003, 2004)
    assert min(small_ranking['Year']) == 2003
    assert max(small_ranking['Year']) == 2004


# Test function co2_reduction_ranking()
def test_co2_reduction_ranking_5_countries(dummy_merged):
    small_ranking = co2_reduction_ranking(dummy_merged, 2003, 1)
    assert len(small_ranking[0]) == 5
    assert len(small_ranking[1]) == 5


def test_co2_reduction_ranking_results_monotonic(dummy_merged):
    small_ranking = co2_reduction_ranking(dummy_merged, 2003, 1)
    assert small_ranking[0].iloc[:, 0].is_monotonic_increasing
    assert small_ranking[1].iloc[:, 0].is_monotonic_decreasing


# Run the tests
if __name__ == '__main__':
    pytest.main()

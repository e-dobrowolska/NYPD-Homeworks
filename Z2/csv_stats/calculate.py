from csv_stats import columns_csv
from statistics import mean, median, stdev

def mean_csv(df):
    header = []
    means = []
    columns = columns_csv(df)
    for column in columns:
        if type(column[1]) == float: # I assume that the type of all elements in a given column is the same
            header.append(column[0])
            means.append(mean(column[1:]))
    return list((header, means))

def median_csv(df):
    header = []
    medians = []
    columns = columns_csv(df)
    for column in columns:
        if type(column[1]) == float: # I assume that the type of all elements in a given column is the same
            header.append(column[0])
            medians.append(median(column[1:]))
    return list((header, medians))

def std_csv(df):
    header = []
    stdevs = []
    columns = columns_csv(df)
    for column in columns:
        if type(column[1]) == float:  # I assume that the type of all elements in a given column is the same
            header.append(column[0])
            stdevs.append(stdev(column[1:]))
    return list((header, stdevs))

def calculate_stats(df):
    header = ['Stats/Columns:']

    means = ['mean']
    mean_stat = mean_csv(df)
    header.extend(mean_stat[0])
    means.extend(mean_stat[1])

    medians = ['median']
    median_stat = median_csv(df)
    medians.extend(median_stat[1])

    stdevs = ['std']
    stdevs_stat = std_csv(df)
    stdevs.extend(stdevs_stat[1])

    output = [header, means, medians, stdevs]
    return output
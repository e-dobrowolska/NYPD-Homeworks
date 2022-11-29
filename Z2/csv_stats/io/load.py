import csv
from contextlib import suppress

def load_csv(path):
    with open(path, 'r') as file:
        csvfile = csv.reader(file)
        df = []
        for row in csvfile:
            df.append(row)
    return df

def columns_csv(df):
    columns = []
    for cols in range(0, len(df[0])):
        current_column = []
        for row in df:
            value = row[cols]
            try:
                value = float(value)
            except:
                pass
            current_column.append(value)
        columns.append(current_column)

    return columns
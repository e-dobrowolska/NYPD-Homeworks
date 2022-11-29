import csv

def save_csv(file_to_save, path):
    with open(path, 'w', newline='') as file:
        csvfile = csv.writer(file)
        for row in file_to_save:
            csvfile.writerow(row)
    return
import csv

def read_threshold(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        float_values = [float(value) for row in reader for value in row]
        return float_values
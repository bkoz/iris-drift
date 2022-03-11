import csv
from typing import List
import numpy as np
import json
from numpy import size

#
# Read the Iris data from a csv file 
# and dump the resulting json object so
# it can be used as a request payload.
#
def build_dict(filename: str) -> dict:
    """
    Convert the Iris CSV data file to a python dictionary.
    """    
    a=[]
    with open(filename, newline='') as csvfile:
        c = csvfile
        reader = csv.DictReader(csvfile)
        for row in reader:
            vec = [float(row["sl"]), float(row["sw"]), float(row["pl"]), float(row["pw"])]
            a.append(vec)

    features=["Sepal length","Sepal width","Petal length", "Petal Width"]
    d = dict(data=dict(names=features, ndarray=a))
    return d


d = build_dict('iris-labeled-data.csv')

print(json.dumps(d))

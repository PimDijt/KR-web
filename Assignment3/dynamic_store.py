from rdfs_rules import *
import itertools

functions = [a for a in dir(rdfs_rules) if  a.startswith('rdfs')]

dynamic_store = {}

with open('testFile.csv','r') as f:
    tripStoreCl = set()
    lines = f.read().splitlines()
    for line in lines:
        s,p,o = line.split(" ")
        tripStoreCl.add((s,p,o))
    print("Standard: ")
    for item in sorted(list(tripStoreCl)):
        print(item)

    for i in itertools.permutations(functions):
        print(i)
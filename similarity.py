import pickle
import sys
import requests
import urllib.parse

with open('dbo_dict.pickle', 'rb') as f:
    dbo_dict = pickle.load(f)

with open('dbtune_dict.pickle', 'rb') as f:
    dbtune_dict = pickle.load(f)

def get_label(term):
    url = "https://hdt.lod.labs.vu.nl/triple?p=rdfs:label&s="+urllib.parse.quote_plus(term)
    r = requests.get(url)
    body = r.content.strip().splitlines()
    for line in body:
        line = line.split()
        object = bytes.decode(line[2])
        index = 3
        while index < (len(line)-2):
            object += bytes.decode(line[index])
            index += 1

        if "@" in object:
            object = object.split("@")
            if object[1] == "en":
                return object[0]
        else:
            object = object.split("^")
            return object[0]

for item in dbo_dict:
    term = item["s"]
    label = get_label(term)
    for item2 in dbtune_dict:
        term2 = item2["s"]
        label2 = get_label(term2)
        print("{} --> {}".format(label, label2))
    sys.exit()

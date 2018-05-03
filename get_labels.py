import pickle
import sys
import requests
import urllib.parse

with open('dbo_dict.pickle', 'rb') as f:
    dbo_dict = pickle.load(f)

with open('dbtune_dict.pickle', 'rb') as f:
    dbtune_dict = pickle.load(f)

result = []

def get_label(term):
    url = "https://hdt.lod.labs.vu.nl/triple?p=rdfs:label&s="+urllib.parse.quote_plus(term)
    print(url)
    r = requests.get(url)
    body = r.content.strip().splitlines()
    for line in body:
        line = line.split()
        triple = {}
        triple["s"] = bytes.decode(line[0])
        triple["p"] = bytes.decode(line[1])
        triple["o"] = bytes.decode(line[2])
        result.append(triple)

count = 0
for item in dbo_dict:
    term = item["s"]
    print("{} / {}".format(count, len(dbo_dict)))
    count += 1
    get_label(term)

with open('dbo_labels.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

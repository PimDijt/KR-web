import os
import numpy as np

feature_column = [
    "rdf:type",
    "rdf:property",
    "rdf:value",
    "rdfs:label",
    "rdfs:range",
    "rdfs:domain",
    "rdfs:subClassOf",
    "rdfs:subPropertyOf",
    "rdfs:seeAlso",
    "rdfs:isDefinedBy",
]

feature_column_url = [
    "<http://wwww3org/1999/02/22-rdf-syntax-ns#type>",
    "<http://www.w3.org/1999/02/22-rdf-syntax-ns#Property>",
    "<http://wwww3org/1999/02/22-rdf-syntax-ns#value>",
    "<http://wwww3org/2000/01/rdf-schema#label>",
    "<http://wwww3org/2000/01/rdf-schema#range>",
    "<http://wwww3org/2000/01/rdf-schema#domain>",
    "<http://wwww3org/2000/01/rdf-schema#subClassOf>",
    "<http://www.w3.org/2000/01/rdf-schema#subPropertyOf>",
    "<http://wwww3org/2000/01/rdf-schema#seeAlso>",
    "<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>",
]

rule_mapping = {
    "trans" : ["rdfs5", "rdfs11"],
    "dora" : ["rdfs2", "rdfs3"],
    "rest" : ["rdfs7", "rdfs9"],
}

features = []
targets = []

for fn in os.listdir('data/'):
    with open('data/'+fn,'r', encoding="utf8") as f:
        tripStoreEx = {'s':{}, 'p':{}, 'o':{}, }


        feature = np.zeros(len(feature_column), dtype=int)
        count = 0
        lines = f.read().replace(".", "").splitlines()
        for line in lines:
            count += 1
            line = line.split()
            s = line[0]
            p = line[1]
            o = " ".join([x for x in line[2:len(line)]])
            if p in feature_column_url or o in feature_column_url:
                feature[feature_column_url.index(p)] += 1

            if p not in tripStoreEx['p'].keys():
                tripStoreEx['p'][p] = {}
                tripStoreEx['p'][p]['s'] = {}
                tripStoreEx['p'][p]['o'] = {}
            if s not in tripStoreEx['p'][p]['s'].keys():
                tripStoreEx['p'][p]['s'][s] = set()
            if o not in tripStoreEx['p'][p]['o'].keys():
                tripStoreEx['p'][p]['o'][o] = set()
            tripStoreEx['p'][p]['s'][s].add(o)
            tripStoreEx['p'][p]['o'][o].add(s)

    output = []
    for p in tripStoreEx['p'].keys():
        for s in tripStoreEx['p'][p]['s'].keys():
            for o in tripStoreEx['p'][p]['s'][s]:
                output.append(s+" "+p+" "+o)
    output = sorted(output)
    #for line in output:
        #print(line)
    features.append((feature/count).tolist())
print(features)

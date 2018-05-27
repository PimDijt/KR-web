import os
import sys
import numpy as np
from rules import *

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
    "<http://wwww3org/1999/02/22-rdf-syntax-ns#type>", #Zijn de URL bewust fout?
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

feature_column_low = [
    "type",
    "property",
    "value",
    "label",
    "range",
    "domain",
    "subclassof",
    "subpropertyof",
    "seealso",
    "isdefinedby",
]

rule_mapping = {
    "subs_subSome" : ["rdfs5", "rdfs11"],
    "subs_dora" : ["rdfs2", "rdfs3"],
    "subs_rest" : ["rdfs7", "rdfs9"],
}

rule_input_mapping = {
    "subs_subSome" : ["rdfs:subPropertyOf", "rdfs:subClassOf"],
    "subs_dora" : ["rdfs:domain", "rdfs:range"],
    "subs_rest" : ["rdfs:subPropertyOf", "rdfs:subClassOf"],
}

features = []
targets = []

rules = rules()

def get_input_nums(tripStore, pred):
    counts = np.zeros(len(pred), dtype=int)
    for i in range(0, len(pred)):
        for p in tripStoreEx['p'].keys():
            for s in tripStoreEx['p'][p]['s'].keys():
                for o in tripStoreEx['p'][p]['s'][s]:
                    if p == pred[i]:
                        counts[i] += 1
    return counts

def create_list(tripStore):
    list = []
    for p in tripStore['p'].keys():
        for s in tripStore['p'][p]['s'].keys():
            for o in tripStore['p'][p]['s'][s]:
                list.append([s, p, o])
    return list

def create_output(tripStore):
    output = []
    for p in tripStoreEx['p'].keys():
        for s in tripStoreEx['p'][p]['s'].keys():
            for o in tripStoreEx['p'][p]['s'][s]:
                output.append(s+" "+p+" "+o)
    output = sorted(output)
    return output


def calculate_feature(list):
    count = 0
    feature = np.zeros(len(feature_column), dtype=int)
    for r in list:
        count += 1
        if r[1] in feature_column or r[2] in feature_column_url: #Moet dit niet r[1] r[2] zijn?
            feature[feature_column.index(r[1])] += 1
    return (feature/count).tolist()

def perform_rules(tripStoreEx, rules1, rules2):
    tripStoreNew = tripStoreEx
    for r in rules1:
        method = getattr(rules, r)
        tripStoreNew, _newFact = method(tripStoreNew)
    for r in rules2:
        method = getattr(rules, r)
        tripStoreNew, _newFact = method(tripStoreNew)
    return tripStoreNew


#for fn in os.listdir('data/'):
for i in range(1):
    fn = sys.argv[1]+'.nt'
    with open('data2/'+fn,'r', encoding="utf8") as f:
    #with open('testFile.csv', encoding="utf8") as f:
        tripStoreEx = {'s':{}, 'p':{}, 'o':{}, }

        lines = f.read().replace(".", "").splitlines()
        for line in lines:
            line2 = line
            line = line.split()
            try:
                s = line[0]
                p = line[1]
                o = " ".join([x for x in line[2:len(line)]])

                for _p in feature_column_low:
                    if _p in p.lower():
                        p = feature_column[feature_column_low.index(_p)]


                #if p in feature_column_url:
                #    p = feature_column[feature_column_low.index(p)]


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
            except IndexError:
                continue

    trip_list = create_list(tripStoreEx)
    feature = calculate_feature(trip_list)


    # get targets
    tripStoreNew = copy.deepcopy(tripStoreEx)
    tripStoreNew = perform_rules(tripStoreNew, ["ssubs_subSome"], ["ssubs_dora", "ssubs_rest"])
    trip_list_1 = create_list(tripStoreNew)
    new_feature_1 = calculate_feature(trip_list_1)

    tripStoreNew = copy.deepcopy(tripStoreEx)
    tripStoreNew = perform_rules(tripStoreNew, ["ssubs_dora", "ssubs_rest"], ["ssubs_subSome"])
    trip_list_2 = create_list(tripStoreNew)
    new_feature_2 = calculate_feature(trip_list_2)

    if len(trip_list_1) < len(trip_list) or len(trip_list_2) < len(trip_list):
        features.append(feature)
        print(feature)
        print(len(trip_list_1)-len(trip_list))
        print(new_feature_1)
        print(len(trip_list_2)-len(trip_list))
        print(new_feature_2)
    else:
        os.remove('data2/'+fn)
        print("Remove")

import os
import sys
import numpy as np
from rules import *

score_feature = [
    3,
    4,
    4,
    1,
    1,
    2,
    2,
    5,
    5
]

feature_column = [
    "rdf:type",
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


def calculate_feature(list, rel):
    count = 0
    feature = np.zeros(len(feature_column), dtype=int)
    for r in list:
        count += 1
        if r[0] in feature_column: #Moet dit niet r[1] r[2] zijn?
            feature[feature_column.index(r[0])] += 1
        if r[1] in feature_column: #Moet dit niet r[1] r[2] zijn?
            feature[feature_column.index(r[1])] += 1
        if r[2] in feature_column: #Moet dit niet r[1] r[2] zijn?
            feature[feature_column.index(r[2])] += 1
    if rel:
        return (feature/count).tolist()
    return (feature).tolist()

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
fns = sys.argv[1]+'/'+sys.argv[2]
fn = fns+'.nt'
with open('dataL/'+fn,'r', encoding="utf8") as f:
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
                if _p in s.lower():
                    s = feature_column[feature_column_low.index(_p)]
                if _p in p.lower():
                    p = feature_column[feature_column_low.index(_p)]
                if _p in o.lower():
                    o = feature_column[feature_column_low.index(_p)]

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
feature = calculate_feature(trip_list, True)

# get targets
tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["ssubs_subSome"], ["ssubs_dora", "ssubs_heritage"])
trip_list_1 = create_list(tripStoreNew)
new_feature_1 = calculate_feature(trip_list_1, False)

tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["ssubs_dora", "ssubs_heritage"], ["ssubs_subSome"])
trip_list_2 = create_list(tripStoreNew)
new_feature_2 = calculate_feature(trip_list_2, False)

scoreA = 0
scoreB = 0
for i in range(len(new_feature_1)):
    tmp = new_feature_1[i]-feature[i]
    scoreA += tmp*score_feature[i]
for i in range(len(new_feature_2)):
    tmp = new_feature_2[i]-feature[i]
    scoreB += tmp*score_feature[i]

res = ""
if scoreA>scoreB:
    res = "A"
if scoreA<scoreB:
    res = "B"
if scoreA!=scoreB or True:
    #features.append(feature)
    print(feature)
    print(res)
    #print(len(trip_list_1)-len(trip_list))
    #print(new_feature_1)
    #print(len(trip_list_2)-len(trip_list))
    #print(new_feature_2)
    #with open('dataL/'+fns+'1.nt','w', encoding="utf8") as f:
    #    for t in trip_list_1:
    #        f.write("%s %s %s ."%(t[0], t[1], t[2]))
    #with open('dataL/'+fns+'2.nt','w', encoding="utf8") as f:
    #    for t in trip_list_2:
    #        f.write("%s %s %s ."%(t[0], t[1], t[2]))
#os.remove('dataL/'+fn)
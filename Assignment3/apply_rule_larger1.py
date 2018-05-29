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

score_feature2 = [
    6,
    8,
    8,
    2,
    2,
    4,
    4,
    10,
    10
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
with open('dataL2/'+fn,'r', encoding="utf8") as f:
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
feature2 = calculate_feature(trip_list, False)


# get targets
tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_subSome"], ["lsubs_dora", "lsubs_heritage"])
trip_list_1a = create_list(tripStoreNew)
new_feature_1a = calculate_feature(trip_list_1a, False)
tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_subSome"], [])
trip_list_1b = create_list(tripStoreNew)
new_feature_1b = calculate_feature(trip_list_1b, False)

tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_dora"], ["lsubs_heritage", "lsubs_subSome"])
trip_list_2a = create_list(tripStoreNew)
new_feature_2a = calculate_feature(trip_list_2a, False)
tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_dora"], [])
trip_list_2b = create_list(tripStoreNew)
new_feature_2b = calculate_feature(trip_list_2b, False)

tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_heritage"], ["lsubs_dora", "lsubs_subSome"])
trip_list_3a = create_list(tripStoreNew)
new_feature_3a = calculate_feature(trip_list_3a, False)
tripStoreNew = copy.deepcopy(tripStoreEx)
tripStoreNew = perform_rules(tripStoreNew, ["lsubs_heritage"], [])
trip_list_3b = create_list(tripStoreNew)
new_feature_3b = calculate_feature(trip_list_3b, False)

scoreAa = 0
scoreBa = 0
scoreCa = 0
if len(trip_list_1a)>1:
    for i in range(len(feature)):
        tmp = new_feature_1a[i]-feature[i]
        scoreAa += tmp*score_feature[i]
    scoreAa-=np.log(len(trip_list_1a)-len(trip_list)+1)
    scoreAa=float(scoreAa)/np.log(len(trip_list_1a))
if len(trip_list_2a)>1:
    for i in range(len(feature)):
        tmp = new_feature_2a[i]-feature[i]
        scoreBa += tmp*score_feature[i]
    scoreBa-=np.log(len(trip_list_2a)-len(trip_list)+1)
    scoreBa=float(scoreBa)/np.log(len(trip_list_2a))
if len(trip_list_3a)>1:
    for i in range(len(feature)):
        tmp = new_feature_3a[i]-feature[i]
        scoreCa += tmp*score_feature[i]
    scoreCa-=np.log(len(trip_list_3a)-len(trip_list)+1)
    scoreCa=float(scoreCa)/np.log(len(trip_list_3a))

scoreAb = 0
scoreBb = 0
scoreCb = 0
if len(trip_list_1b)>1:
    for i in range(len(feature)):
        tmp = new_feature_1b[i]-feature[i]
        scoreAb += tmp*score_feature[i]
    scoreAb-=np.log(len(trip_list_1b)-len(trip_list)+1)
    scoreAb=float(scoreAb)/np.log(len(trip_list_1b))
if len(trip_list_2b)>1:
    for i in range(len(feature)):
        tmp = new_feature_2b[i]-feature[i]
        scoreBb += tmp*score_feature[i]
    scoreBb-=np.log(len(trip_list_2b)-len(trip_list)+1)
    scoreBb=float(scoreBb)/np.log(len(trip_list_2b))
if len(trip_list_3b)>1:
    for i in range(len(feature)):
        tmp = new_feature_3b[i]-feature[i]
        scoreCb += tmp*score_feature[i]
    scoreCb-=np.log(len(trip_list_3b)-len(trip_list)+1)
    scoreCb=float(scoreCb)/np.log(len(trip_list_3b))

scoreAa1 = 0
scoreBa1 = 0
scoreCa1 = 0
if len(trip_list_1a)>1:
    for i in range(len(feature)):
        tmp = new_feature_1a[i]-feature[i]
        scoreAa1 += tmp*score_feature2[i]
    scoreAa1-=np.log(len(trip_list_1a)-len(trip_list)+1)
    scoreAa1=float(scoreAa1)/np.log(len(trip_list_1a))
if len(trip_list_2a)>1:
    for i in range(len(feature)):
        tmp = new_feature_2a[i]-feature[i]
        scoreBa1 += tmp*score_feature2[i]
    scoreBa1-=np.log(len(trip_list_2a)-len(trip_list)+1)
    scoreBa1=float(scoreBa1)/np.log(len(trip_list_2a))
if len(trip_list_3a)>1:
    for i in range(len(feature)):
        tmp = new_feature_3a[i]-feature[i]
        scoreCa1 += tmp*score_feature2[i]
    scoreCa1-=np.log(len(trip_list_3a)-len(trip_list)+1)
    scoreCa1=float(scoreCa1)/np.log(len(trip_list_3a))

scoreAb1 = 0
scoreBb1 = 0
scoreCb1 = 0
if len(trip_list_1b)>1:
    for i in range(len(feature)):
        tmp = new_feature_1b[i]-feature[i]
        scoreAb1 += tmp*score_feature2[i]
    scoreAb1-=np.log(len(trip_list_1b)-len(trip_list)+1)
    scoreAb1=float(scoreAb1)/np.log(len(trip_list_1b))
if len(trip_list_2b)>1:
    for i in range(len(feature)):
        tmp = new_feature_2b[i]-feature[i]
        scoreBb1 += tmp*score_feature2[i]
    scoreBb1-=np.log(len(trip_list_2b)-len(trip_list)+1)
    scoreBb1=float(scoreBb1)/np.log(len(trip_list_2b))
if len(trip_list_3b)>1:
    for i in range(len(feature)):
        tmp = new_feature_3b[i]-feature[i]
        scoreCb1 += tmp*score_feature2[i]
    scoreCb1-=np.log(len(trip_list_3b)-len(trip_list)+1)
    scoreCb1=float(scoreCb1)/np.log(len(trip_list_3b))

resa = ""
resb = ""
resa1 = ""
resb1 = ""
if scoreAa>scoreBa and scoreAa>scoreCa:
    resa = "A"
if scoreBa>scoreAa and scoreBa>scoreCa:
    resa = "B"
if scoreCa>scoreAa and scoreCa>scoreAa:
    resa = "C"

if scoreAb>scoreBb and scoreAb>scoreCb:
    resb = "A"
if scoreBb>scoreAb and scoreBb>scoreCb:
    resb = "B"
if scoreCb>scoreAb and scoreCb>scoreAb:
    resb = "C"

if scoreAa1>scoreBa1 and scoreAa1>scoreCa1:
    resa1 = "A"
if scoreBa1>scoreAa1 and scoreBa1>scoreCa1:
    resa1 = "B"
if scoreCa1>scoreAa1 and scoreCa1>scoreAa1:
    resa1 = "C"
if scoreAb1>scoreBb1 and scoreAb1>scoreCb1:
    resb1 = "A"
if scoreBb1>scoreAb1 and scoreBb1>scoreCb1:
    resb1 = "B"
if scoreCb1>scoreAb1 and scoreCb1>scoreAb1:
    resb1 = "C"
feature.append(resa)
feature.append(resb)
feature.append(resa1)
feature.append(resb1)

if scoreAa!=scoreBa or scoreAb!=scoreBb:
    #features.append(feature)
    print(feature)
    #print(res)
    #print(len(trip_list_1)-len(trip_list))
    #print(new_feature_1)
    #print(len(trip_list_2)-len(trip_list))
    #print(new_feature_2)
    if scoreAa!=scoreBa or scoreAa!=scoreCa or scoreCa!=scoreBa:
        with open('dataL2/'+fns+'1a.nt','w', encoding="utf8") as f:
            for t in trip_list_1a:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
        with open('dataL2/'+fns+'2a.nt','w', encoding="utf8") as f:
            for t in trip_list_2a:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
    if scoreAb!=scoreBb or scoreAb!=scoreCb or scoreCb!=scoreBb:
        with open('dataL2/'+fns+'1b.nt','w', encoding="utf8") as f:
            for t in trip_list_1b:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
        with open('dataL2/'+fns+'2b.nt','w', encoding="utf8") as f:
            for t in trip_list_2b:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
    if scoreAa1!=scoreBa1 or scoreAa1!=scoreCa1 or scoreCa1!=scoreBa1:
        with open('dataL2/'+fns+'1a1.nt','w', encoding="utf8") as f:
            for t in trip_list_1a:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
        with open('dataL2/'+fns+'2a1.nt','w', encoding="utf8") as f:
            for t in trip_list_2a:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
    if scoreAb1!=scoreBb1 or scoreAb1!=scoreCb1 or scoreCb1!=scoreBb1:
        with open('dataL2/'+fns+'1b1.nt','w', encoding="utf8") as f:
            for t in trip_list_1b:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
        with open('dataL2/'+fns+'2b1.nt','w', encoding="utf8") as f:
            for t in trip_list_2b:
                f.write("%s %s %s ."%(t[0], t[1], t[2]))
print('dataL2/'+fn)
os.remove('dataL2/'+fn)
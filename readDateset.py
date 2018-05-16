import itertools
from rdfs_rules import *

def printr(listr):
    tmp = []
    for item in listr:
        tmp.append(''.join(item.pair))
    for item in sorted(tmp):
        print(item)

functions = [a for a in dir(rdfs_rules) if  a.startswith('rdfs')]

dynamic_store = {}

with open('testFile.csv','r') as f:
    tripStoreCl = set()
    lines = f.read().splitlines()
    for line in lines:
        tripStoreCl.add(rdfs_rules(line.split(" ")))
    print("Standard: ")
    printr(tripStoreCl)

    for perm in list(itertools.permutations(functions)):
        if perm[0]!='rdfs13_literal':
            continue
        newFact = True
        tripStore = set(list(tripStoreCl)[:])
        rules=0
        while newFact:
            newFact = False
            for func in perm:
                tripStoreNew = []
                tmp = set()
                for item in tripStore:
                    tmp.add(''.join(item.pair))
                srtTripStore = ''.join(sorted(list(tmp)))
                #if srtTripStore in dynamic_store.keys() and func in dynamic_store[srtTripStore].keys():
                #    tripStoreNew = dynamic_store[srtTripStore][func][:]
                #else:
                for tripA in tripStore:
                    go = True
                    method = getattr(tripA, func)
                    retlist = method(tripStore)
                    if retlist:
                        for ret in retlist:
                            ret = rdfs_rules(ret.split(" "))
                            #if ret in list(tripStore)+tripStoreNew:
                            #    break
                            for tripX in list(tripStore)+tripStoreNew:
                                if tripX.equals(ret):
                                    go = False
                                    break
                            if go:
                                tripStoreNew.append(ret)
                                newFact = True
                if srtTripStore not in dynamic_store.keys():
                    dynamic_store[srtTripStore] = {}
                if func not in dynamic_store[srtTripStore].keys():
                    dynamic_store[srtTripStore][func] = []                    
                dynamic_store[srtTripStore][func] = tripStoreNew
                if len(tripStoreNew)>0:
                    rules+=1
                    #print("Rule: %s worked"%func)
                    tripStore = set(list(tripStore)+tripStoreNew)
        #printr(tripStore)
        print(rules, len(tripStore), perm)
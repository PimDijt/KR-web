import itertools
<<<<<<< HEAD
from rdfs_rules import *
=======
import random
import copy
from ruler import *
>>>>>>> 12d871640b03503594bd4aba985eebd0eb7b82cb

def printr(listr):
    tmp = []
    for item in listr:
        tmp.append(''.join(item.pair))
    for item in sorted(tmp):
        print(item)

functions = [a for a in dir(rdfs_rules) if  a.startswith('rdfs')]

dynamic_store = {}

<<<<<<< HEAD
with open('testFile.csv','r') as f:
    tripStoreCl = set()
    lines = f.read().splitlines()
    for line in lines:
        tripStoreCl.add(rdfs_rules(line.split(" ")))
    print("Standard: ")
    printr(tripStoreCl)
=======
functions = [a for a in dir(ruler) if a.startswith('rdfs')]

with open('testFile.csv','r') as f:
    tripStoreClean = {}
    tripStoreClean['s'] = {}
    tripStoreClean['p'] = {}
    tripStoreClean['o'] = {}
    lines = f.read().splitlines()
    for line in lines:
        s,p,o = line.split(" ")
        if p not in tripStoreClean['p'].keys():
            tripStoreClean['p'][p] = {}
            tripStoreClean['p'][p]['s'] = {}
            tripStoreClean['p'][p]['o'] = {}
        if s not in tripStoreClean['p'][p]['s'].keys():
            tripStoreClean['p'][p]['s'][s] = []
        if o not in tripStoreClean['p'][p]['o'].keys():
            tripStoreClean['p'][p]['o'][o] = []
        tripStoreClean['p'][p]['o'][o].append(s)
        tripStoreClean['p'][p]['s'][s].append(o)
    print("Standard: ", tripStoreClean['p'].keys())

    for randomPerm in range(100):
        random.shuffle(functions)
        newFact = True
        tripStore = copy.deepcopy(tripStoreClean)
        rules=0
        while newFact:
            newFact = False
            for func in functions:
                tripStoreNew = {'s':{}, 'p':{}, 'o':{}}
                '''for tripA in tripStore:
                    go = True                       
                    method = getattr(tripA, func)
                    retlist = method(tripStore)
                    if retlist:
                        for ret in retlist:
                            ret = ruler(ret.split(" "))
                            for tripX in (tripStore+tripStoreNew):
                                if tripX.equals(ret):
                                    go = False
                                    break #We found one match so we dont have to do the full union of old+new facts
                            #for tripX in tripStoreNew:
                            #    if tripX.equals(ret):
                            #        go = False
                            if go:
                                tripStoreNew.append(ret)
                                newFact = True'''
                if len(tripStoreNew['s'])+len(tripStoreNew['p'])+len(tripStoreNew['o'])>0:
                    rules+=1
                    #print("Rule: %s worked"%func)
                    tripStore += tripStoreNew
>>>>>>> 12d871640b03503594bd4aba985eebd0eb7b82cb

    '''random.shuffle(functions)#list(itertools.permutations(functions)):
    for randomPerm in range(100):#functions:#list(itertools.permutations(functions)):
        random.shuffle(functions)#list(itertools.permutations(functions)):
        newFact = True
        tripStore = set(list(tripStoreCl)[:])
        rules=0
        while newFact:
            newFact = False
            for func in functions:
                tripStoreNew = []
                tmp = set()
                for item in tripStore:
                    tmp.add(''.join(item.pair))
                srtTripStore = ''.join(sorted(list(tmp)))
                if srtTripStore in dynamic_store.keys() and func in dynamic_store[srtTripStore].keys():
                    tripStoreNew = dynamic_store[srtTripStore][func][:]
                else:
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
<<<<<<< HEAD
                    print("Rule: %s worked"%func)
                    tripStore = set(list(tripStore)+tripStoreNew)
        #printr(tripStore)
        print(rules, len(tripStore), perm)
=======
                    #print("Rule: %s worked"%func)
                    tripStore += tripStoreNew
        #printr(tripStore)'''
    #print(rules, randomPerm, len(tripStore), functions)
>>>>>>> 12d871640b03503594bd4aba985eebd0eb7b82cb

import itertools
import random
import copy
from ruler import *

def printr(listr):
    for item in listr:
        print(item.pair)

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
            '''for func in functions:
                tripStoreNew = []
                for tripA in tripStore:
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
                                newFact = True
                if len(tripStoreNew)>0:
                    rules+=1
                    #print("Rule: %s worked"%func)
                    tripStore += tripStoreNew'''

    '''random.shuffle(functions)#list(itertools.permutations(functions)):
    for randomPerm in range(100):#functions:#list(itertools.permutations(functions)):
        random.shuffle(functions)#list(itertools.permutations(functions)):
        newFact = True
        tripStore = tripStoreCl[:]
        rules=0
        while newFact:
            newFact = False
            for func in functions:
                tripStoreNew = []
                for tripA in tripStore:
                    go = True                       
                    method = getattr(tripA, func)
                    retlist = method(tripStore)
                    if retlist:
                        for ret in retlist:
                            ret = ruler(ret.split(" "))
                            for tripX in tripStore:
                                if tripX.equals(ret):
                                    go = False
                            for tripX in tripStoreNew:
                                if tripX.equals(ret):
                                    go = False
                            if go:
                                tripStoreNew.append(ret)
                                newFact = True
                if len(tripStoreNew)>0:
                    rules+=1
                    #print("Rule: %s worked"%func)
                    tripStore += tripStoreNew
        #printr(tripStore)'''
    #print(rules, randomPerm, len(tripStore), functions)
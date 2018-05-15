import itertools
from ruler import *

def printr(listr):
    for item in listr:
        print(item.pair)

functions = [a for a in dir(ruler) if  a.startswith('rdfs')]
with open('testFile.csv','r') as f:
    tripStoreCl = []
    lines = f.read().splitlines()
    for line in lines:
        tripStoreCl.append(ruler(line.split(" ")))
    print("Standard: ", tripStoreCl)

    for perm in list(itertools.permutations(functions)):
        newFact = True
        tripStore = tripStoreCl[:]
        while newFact:
            newFact = False
            for func in perm:
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
                '''if func[0]==1:
                        #print("A: ", tripA.pair)
                        for tripB in tripStore:
                            #print(tripB.pair)
                            ret = tripA.classOf(tripB)
                            if ret is not None:
                                ret = ruler(ret)
                                for tripX in tripStore:
                                    if tripX.equals(ret):
                                        go = False
                                for tripX in tripStoreNew:
                                    if tripX.equals(ret):
                                        go = False
                                if go:
                                    #print("Go")
                                    tripStoreNew.append(ret)
                                    newFact = True
                elif func[0]==0:
                    for tripA in tripStore:
                        for tripB in tripStore:
                            go = True                       
                            ret = tripA.classrel(tripB)
                            if ret is not None:
                                ret = ruler(ret)
                                for tripX in tripStore:
                                    if tripX.equals(ret):
                                        go = False
                                for tripX in tripStoreNew:
                                    if tripX.equals(ret):
                                        go = False
                                if go:
                                    tripStoreNew.append(ret)
                                    newFact = True'''
                if len(tripStoreNew)>0:
                    print("Rule: %s worked"%func)
                    tripStore += tripStoreNew
        printr(tripStore)
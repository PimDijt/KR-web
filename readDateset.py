import itertools
from ruler import *

functions = [[1,2], [0,2]]
with open('testFile.csv','r') as f:
    tripStore = []
    lines = f.read().splitlines()
    for line in lines:
        tripStore.append(ruler(line.split(" ")))
    print("Standard: ", tripStore)

    for perm in list(itertools.permutations(functions)):
        newFact = True
        passVal = 0
        while newFact:
            newFact = False
            for func in perm:
                tripStoreNew = []
                #print(func)
                if func[0]==1:
                    for tripA in tripStore:
                        for tripB in tripStore:
                            ret = tripA.classOf(tripB)
                            if ret is not None:
                                ret = ruler(ret)
                                go = True
                                for tripX in tripStore:
                                    print(tripX.pair,ret.pair)
                                    if tripX.equals(ret):
                                        go = False
                                        print("Boobm")
                                if passVal==2:
                                    exit(-1)
                                for tripX in tripStoreNew:
                                    if tripX.equals(ret):
                                        go = False
                                if go:
                                    tripStoreNew.append(ret)
                                    newFact = True
                '''if func[0]==0:
                    for tripA in tripStore:
                        for tripB in tripStore:
                            tripA.classrel(tripB)
                            if ret is not None:
                                for tripX in tripStore:
                                    if tripX.equals(ret):
                                        continue
                                for tripX in tripStoreNew:
                                    if tripX.equals(ret):
                                        continue
                                tripStoreNew.append(ret)
                                newFact = True'''
                if newFact:
                    for tripX in tripStore:
                        tripStoreNew.append(tripX)
                    tripStore = tripStoreNew
                passVal+=1
        print(tripStore)
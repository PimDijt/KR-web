import itertools
from ruler import *

functions = [[1,2], [0,2]]
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
                go = True                       
                if func[0]==1:
                    for tripA in tripStore:
                        for tripB in tripStore:
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
                                    tripStoreNew.append(ret)
                                    newFact = True
                elif func[0]==0:
                    for tripA in tripStore:
                        for tripB in tripStore:
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
                                    newFact = True
                if go and len(tripStoreNew)>0:
                    print("Rule: %d worked"%func[0])
                    print(tripStoreNew)
                    tripStore += tripStoreNew
from rules import *
import itertools

functions = [a for a in dir(rules) if  a.startswith('subs')]

dynamic_store = {}

rules = rules()

with open('testFile.csv','r') as f:
    tripStoreCl = set()
    tripStoreEx = {'s':{}, 'p':{}, 'o':{}, }
    lines = f.read().splitlines()
    for line in lines:
        s,p,o = line.split(" ")
        tripStoreCl.add((s,p,o))

        '''#Indexing on S
        if s not in tripStoreEx['s'].keys():
            tripStoreEx['s'][s] = {}
            tripStoreEx['s'][s]['p'] = {}
            tripStoreEx['s'][s]['o'] = {}
        if p not in tripStoreEx['s'][s]['p'].keys():
            tripStoreEx['s'][s]['p'][p] = set()
        if o not in tripStoreEx['s'][s]['o'].keys():
            tripStoreEx['s'][s]['o'][o] = set()
        tripStoreEx['s'][s]['p'][p].add(o)
        tripStoreEx['s'][s]['o'][o].add(p)'''

        #Indexing on P
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

        '''#Indexing on O
        if o not in tripStoreEx['o'].keys():
            tripStoreEx['o'][o] = {}
            tripStoreEx['o'][o]['s'] = {}
            tripStoreEx['o'][o]['p'] = {}
        if s not in tripStoreEx['o'][o]['s'].keys():
            tripStoreEx['o'][o]['s'][s] = set()
        if p not in tripStoreEx['o'][o]['p'].keys():
            tripStoreEx['o'][o]['p'][p] = set()
        tripStoreEx['o'][o]['s'][s].add(p)
        tripStoreEx['o'][o]['p'][p].add(s)'''

    output = []
    for p in tripStoreEx['p'].keys():
        for s in tripStoreEx['p'][p]['s'].keys():
            for o in tripStoreEx['p'][p]['s'][s]:
                output.append(s+" "+p+" "+o)
    output = sorted(output)
    for line in output:
        print(line)
    for perm in itertools.permutations(functions):
        print(perm)
        tripStoreNew = copy.deepcopy(tripStoreEx)
        newFact = True
        while newFact:
            newFact = False
            for func in perm:
                method = getattr(rules, func)
                tripStoreNew, newFactT = method(tripStoreNew)
                if newFactT:
                    newFact = True
        output = []
        for p in tripStoreNew['p'].keys():
            for s in tripStoreNew['p'][p]['s'].keys():
                for o in tripStoreNew['p'][p]['s'][s]:
                    output.append(s+" "+p+" "+o)
        output = sorted(output)
        for line in output:
            print(line)
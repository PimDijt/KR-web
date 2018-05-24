import copy

class rules(object):
    s = ""
    p = ""
    o = ""
    pair = ""

    #def __init__(self, pair):
    #    self.s = pair[0]
    #    self.p = pair[1]
    #    self.o = pair[2]
    #    self.pair = pair
    
    def __init__(self):
        self.s = ""
    
    def subs_singleRules(self, current):
        new = copy.deepcopy(current)
        new, rf1 = self.rdfs1_allIsDataType(new)
        new, rf2 = self.rdfs4a_Resource(new)
        new, rf3 = self.rdfs4b_Resource(new)
        return new, (rf1 or rf2 or rf3)

    def subs_dora(self, current):
        new = copy.deepcopy(current)
        new, rf1 = self.rdfs2_domain(new)
        new, rf2 = self.rdfs3_range(new)
        return new, (rf1 or rf2)

    def rdfs1_allIsDataType(self, current):
        new = copy.deepcopy(current)

        keys = set()

        for p in new['p'].keys():
            keys.add(p)
            for s in new['p'][p]['s'].keys():
                keys.add(s)
                for o in new['p'][p]['s'][s]:
                    keys.add(o)

        for key in keys:
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            if key              not in new['p']['rdf:type']['s'].keys():
                new['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Datatype'  not in new['p']['rdf:type']['o'].keys():
                new['p']['rdf:type']['o']['rdfs:Datatype'] = set()
            lens1 = len(new['p']['rdf:type']['s'][key])
            leno1 = len(new['p']['rdf:type']['o']['rdfs:Datatype'])#This one is not needed I think...
            new['p']['rdf:type']['s'][key].add('rdfs:Datatype')
            new['p']['rdf:type']['o']['rdfs:Datatype'].add(key)
            lens2 = len(new['p']['rdf:type']['s'][key])
            leno2 = len(new['p']['rdf:type']['o']['rdfs:Datatype'])
        return new, (lens1!=lens2 or leno1!=leno2)

    def rdfs2_domain(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:domain" and self.s==other.p:
        #            result.add(other.s+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        sset = set(new['p']['rdfs:domain']['s'].keys())
        pset = set(new['p'].keys())
        keys = sset.intersection(pset)
        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:domain']['s'][key]:
                keypairs.add((key,o))

        for p,o in keypairs:
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            for s in new['p'][p]['s'].keys():
                if s    not in new['p']['rdf:type']['s'].keys():
                    new['p']['rdf:type']['s'][s] = set()
                if o    not in new['p']['rdf:type']['o'].keys():
                    new['p']['rdf:type']['o'][o] = set()
                lens1 = len(new['p']['rdf:type']['s'][s])
                leno1 = len(new['p']['rdf:type']['o'][o])#This one is not needed I think...
                new['p']['rdf:type']['s'][s].add(o)
                new['p']['rdf:type']['o'][o].add(s)
                lens2 = len(new['p']['rdf:type']['s'][s])
                leno2 = len(new['p']['rdf:type']['o'][o])
        return new, (lens1!=lens2 or leno1!=leno2)

    def rdfs3_range(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:range" and self.s==other.p:
        #            result.add(other.o+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        sset = set(new['p']['rdfs:domain']['s'].keys())
        pset = set(new['p'].keys())
        keys = sset.intersection(pset)
        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:domain']['s'][key]:
                keypairs.add((key,o))

        for p,o in keypairs:
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            for o2 in new['p'][p]['o'].keys():
                if o2    not in new['p']['rdf:type']['s'].keys():
                    new['p']['rdf:type']['s'][o2] = set()
                if o    not in new['p']['rdf:type']['o'].keys():
                    new['p']['rdf:type']['o'][o] = set()
                lens1 = len(new['p']['rdf:type']['s'][o2])
                leno1 = len(new['p']['rdf:type']['o'][o])#This one is not needed I think...
                new['p']['rdf:type']['s'][o2].add(o)
                new['p']['rdf:type']['o'][o].add(o2)
                lens2 = len(new['p']['rdf:type']['s'][o2])
                leno2 = len(new['p']['rdf:type']['o'][o])
        return new, (lens1!=lens2 or leno1!=leno2)

    def rdfs4a_Resource(self, current):
        new = copy.deepcopy(current)

        keys = set()

        for p in new['p'].keys():
            for s in new['p'][p]['s'].keys():
                keys.add(s)

        for key in keys:
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            if key              not in new['p']['rdf:type']['s'].keys():
                new['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Resource'  not in new['p']['rdf:type']['o'].keys():
                new['p']['rdf:type']['o']['rdfs:Resource'] = set()
            lens1 = len(new['p']['rdf:type']['s'][key])
            leno1 = len(new['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            new['p']['rdf:type']['s'][key].add('rdfs:Resource')
            new['p']['rdf:type']['o']['rdfs:Resource'].add(key)
            lens2 = len(new['p']['rdf:type']['s'][key])
            leno2 = len(new['p']['rdf:type']['o']['rdfs:Resource'])
        return new, (lens1!=lens2 or leno1!=leno2)

    def rdfs4b_Resource(self, current):
        new = copy.deepcopy(current)

        keys = set()

        for p in new['p'].keys():
            for o in new['p'][p]['o'].keys():
                keys.add(o)

        for key in keys:
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            if key              not in new['p']['rdf:type']['s'].keys():
                new['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Resource'  not in new['p']['rdf:type']['o'].keys():
                new['p']['rdf:type']['o']['rdfs:Resource'] = set()
            lens1 = len(new['p']['rdf:type']['s'][key])
            leno1 = len(new['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            new['p']['rdf:type']['s'][key].add('rdfs:Resource')
            new['p']['rdf:type']['o']['rdfs:Resource'].add(key)
            lens2 = len(new['p']['rdf:type']['s'][key])
            leno2 = len(new['p']['rdf:type']['o']['rdfs:Resource'])
        return new, (lens1!=lens2 or leno1!=leno2)

    '''def rdfs5_subProperty(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:subPropertyOf" and other.p=="rdfs:subPropertyOf" and self.s==other.o:
                result.add(self.s+" rdfs:subPropertyOf "+other.o)
        return list(result)

    def rdfs6_typeProperty(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdf:Property":
            result.add(self.s+" rdfs:subPropertyOf "+self.s)
        return list(result)

    def rdfs7_parentSubProperty(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:subPropertyOf" and self.s==other.p:
                result.add(other.s+" "+self.o+" "+other.o)
        return list(result)

    def rdfs8_subClassResource(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdfs:Class":
            result.add(self.s+" rdfs:subClassOf rdfs:Resource")
        return list(result)
    
    def rdfs9_typeOfClass(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:subClassOf" and other.p=="rdf:type" and self.s==other.o:
                result.add(other.s+" rdf:type "+self.o)
        return list(result)

    def rdfs10_subClassSelf(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdfs:Class":
            result.add(self.s+" rdfs:subClassOf "+self.s)
        return list(result)
    
    def rdfs11_subClass(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:subClassOf" and other.p=="rdfs:subClassOf" and self.o==other.s:
                result.add(self.s+" rdfs:subClassOf "+other.o)
        return list(result)'''
    
    #def rdfs12_container(self, current):
    #    #result = set()
    #    #if self.p=="rdf:type" and self.o=="rdfs:ContainerMembershipProperty":
    #    #    result.add(self.s+" rdfs:subPropertyOf rdfs:member")
    #    #return list(result)
    
    #def rdfs13_literal(self, current):
    #    #result = set()
    #    #if self.p=="rdf:type" and self.o=="rdfs:Datatype":
    #    #    result.add(self.s+" rdfs:subClassOf rdfs:Literal")
    #    #return list(result)


    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)


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
        new = self.rdfs1_allIsDataType(current)
        return new

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
            if key not in new['s'].keys():
                new['s'][key] = {}
                new['s'][key]['p'] = {}
                new['s'][key]['o'] = {}
            if 'rdf:type'       not in new['s'][key]['p'].keys():
                new['s'][key]['p']['rdf:type'] = set()
            if 'rdfs:Datatype'  not in new['s'][key]['o'].keys():
                new['s'][key]['o']['rdfs:Datatype'] = set()
            new['s'][key]['o']['rdfs:Datatype'].add('rdf:type')
            new['s'][key]['p']['rdf:type'].add('rdfs:Datatype')
            
            if 'rdf:type' not in new['p'].keys():
                new['p']['rdf:type'] = {}
                new['p']['rdf:type']['s'] = {}
                new['p']['rdf:type']['o'] = {}
            if key              not in new['p']['rdf:type']['s'].keys():
                new['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Datatype'  not in new['p']['rdf:type']['o'].keys():
                new['p']['rdf:type']['o']['rdfs:Datatype'] = set()
            new['p']['rdf:type']['s'][key].add('rdfs:Datatype')
            new['p']['rdf:type']['o']['rdfs:Datatype'].add(key)

            if 'rdfs:Datatype' not in new['o'].keys():
                new['o']['rdfs:Datatype'] = {}
                new['o']['rdfs:Datatype']['s'] = {}
                new['o']['rdfs:Datatype']['p'] = {}
            if key              not in new['o']['rdfs:Datatype']['s'].keys():
                new['o']['rdfs:Datatype']['s'][key] = set()
            if 'rdf:type'       not in new['o']['rdfs:Datatype']['p'].keys():
                new['o']['rdfs:Datatype']['p']['rdf:type'] = set()
            new['o']['rdfs:Datatype']['s'][key].add('rdf:type')
            new['o']['rdfs:Datatype']['p']['rdf:type'].add(key)
        return new

    '''def rdfs2_domain(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:domain" and self.s==other.p:
                result.add(other.s+" rdf:type "+self.o)
        return list(result)

    #def rdfs3_range(self, store):
    #    result = set()
    #    for other in store:
    #        if self.p=="rdfs:range" and self.s==other.p:
    #            result.add(other.o+" rdf:type "+self.o)
    #    return list(result)

    #def rdfs4a_Resource(self, store):
    #    result = set()
    #    result.add(self.s+" a rdfs:Datatype")
    #    return list(result)

    #def rdfs4b_Resource(self, store):
    #    result = set()
    #    result.add(self.o+" a rdfs:Datatype")
    #    return list(result)

    def rdfs5_subProperty(self, store):
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
        return list(result)
    
    #def rdfs12_container(self, store):
    #    result = set()
    #    if self.p=="rdf:type" and self.o=="rdfs:ContainerMembershipProperty":
    #        result.add(self.s+" rdfs:subPropertyOf rdfs:member")
    #    return list(result)
    
    def rdfs13_literal(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdfs:Datatype":
            result.add(self.s+" rdfs:subClassOf rdfs:Literal")
        return list(result)
    
    #def rdfs_bonus1(self, store):
    #    result = set()
    #    if self.p=="a":
    #        result.add(self.s+" rdf:type "+self.o)
    #    return list(result)

    #def rdfs_bonus2(self, store):
    #    result = set()
    #    if self.p=="sc":
    #        result.add(self.s+" rdfs:subClassOf "+self.o)
    #    return list(result)

    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)'''


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
    
    def test_all(self, current):
        new = copy.deepcopy(current)
        new, rf1 = (new, False)#self.rdfs1_allIsDataType(new)
        new, rf2 = self.rdfs2_domain(new)
        new, rf3 = self.rdfs3_range(new)
        new, rf4a = self.rdfs4a_Resource(new)
        new, rf4b = self.rdfs4b_Resource(new)
        new, rf5 = self.rdfs5_subProperty(new)
        new, rf6 = self.rdfs6_typeProperty(new)
        new, rf7 = self.rdfs7_parentSubProperty(new)
        new, rf8 = self.rdfs8_subClassResource(new)
        new, rf9 = self.rdfs9_typeOfClass(new)
        new, rf10 = self.rdfs10_subClassSelf(new)
        new, rf11 = self.rdfs11_subClass(new)
        new, rf12 = self.rdfs12_container(new)
        new, rf13 = self.rdfs13_literal(new)
        return new, (rf1 or rf2 or rf3 or rf4a or rf4b or rf5 or rf6 or rf7 or rf8 or rf9 or rf10 or rf11 or rf12 or rf13)

    def subs_singleRules(self, current):
        new = copy.deepcopy(current)
        rf4a = False
        rf4b = False
        rf6 = False
        rf8 = False
        rf10 = False
        rf12 = False
        rf13 = False
        new, rf1    = self.rdfs1_allIsDataType(new)
        #new, rf4a   = self.rdfs4a_Resource(new)
        #new, rf4b   = self.rdfs4b_Resource(new)
        #new, rf6    = self.rdfs6_typeProperty(new)
        #new, rf8    = self.rdfs8_subClassResource(new)
        #new, rf10   = self.rdfs10_subClassSelf(new)
        #new, rf12   = self.rdfs12_container(new)
        new, rf13   = self.rdfs13_literal(new)
        return new, (rf1 or rf4a or rf4b or rf6 or rf8 or rf10 or rf12 or rf13)

    def subs_dora(self, current):
        new = copy.deepcopy(current)
        new, rf2 = self.rdfs2_domain(new)
        new, rf3 = self.rdfs3_range(new)
        return new, (rf2 or rf3)

    def subs_rest(self, current):
        new = copy.deepcopy(current)
        rf7 = False
        rf9 = False
        new, rf7 = self.rdfs7_parentSubProperty(new)
        new, rf9 = self.rdfs9_typeOfClass(new)
        return new, (rf7 or rf9)

    def subs_subSome(self, current):
        new = copy.deepcopy(current)
        new, rf5 = self.rdfs5_subProperty(new)
        new, rf11 = self.rdfs11_subClass(new)
        return new, (rf5 or rf11)

    def rdfs1_allIsDataType(self, current):
        new = copy.deepcopy(current)

        keys = set()

        changed = False

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
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed

    def rdfs2_domain(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:domain" and self.s==other.p:
        #            result.add(other.s+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        changed = False

        if 'rdfs:domain' in new['p'].keys():
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
                    if (lens1!=lens2 or leno1!=leno2):
                        changed = True
            return new, changed
        else:
            return new, False

    def rdfs3_range(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:range" and self.s==other.p:
        #            result.add(other.o+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        changed = False

        sset = set(new['p']['rdfs:range']['s'].keys())
        pset = set(new['p'].keys())
        keys = sset.intersection(pset)
        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:range']['s'][key]:
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
                if (lens1!=lens2 or leno1!=leno2):
                    changed = True
        return new, changed

    def rdfs4a_Resource(self, current):
        new = copy.deepcopy(current)

        changed = False

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
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed

    def rdfs4b_Resource(self, current):
        new = copy.deepcopy(current)

        changed = False

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
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed

    def rdfs5_subProperty(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subPropertyOf" and other.p=="rdfs:subPropertyOf" and self.s==other.o:
        #        result.add(self.s+" rdfs:subPropertyOf "+other.o)
        #return list(result)'''

        new = copy.deepcopy(current)

        changed = False

        keys = set()

        sset = set(new['p']['rdfs:subPropertyOf']['s'].keys())
        oset = set(new['p']['rdfs:subPropertyOf']['o'].keys())
        keys = sset.intersection(oset)

        for key in keys:
            for o in new['p']['rdfs:subPropertyOf']['s'][key]:
                for s in new['p']['rdfs:subPropertyOf']['o'][key]:
                    lens1 = len(new['p']['rdfs:subPropertyOf']['s'][s])
                    leno1 = len(new['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    new['p']['rdfs:subPropertyOf']['s'][s].add(o)
                    new['p']['rdfs:subPropertyOf']['o'][o].add(s)
                    lens2 = len(new['p']['rdfs:subPropertyOf']['s'][s])
                    leno2 = len(new['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    if (lens1!=lens2 or leno1!=leno2):
                        changed = True
        return new, changed

    def rdfs6_typeProperty(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdf:Property":
        #    result.add(self.s+" rdfs:subPropertyOf "+self.s)
        #return list(result)
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        if 'rdf:Property' in new['p']['rdf:type']['o'].keys():
            for s in new['p']['rdf:type']['o']['rdf:Property']:
                keys.add(s)
        else:
            return new, False

        for key in keys:
            if 'rdfs:subPropertyOf' not in new['p'].keys():
                new['p']['rdfs:subPropertyOf'] = {}
                new['p']['rdfs:subPropertyOf']['s'] = {}
                new['p']['rdfs:subPropertyOf']['o'] = {}
            if key  not in new['p']['rdfs:subPropertyOf']['s'].keys():
                new['p']['rdfs:subPropertyOf']['s'][key] = set()
            if key  not in new['p']['rdfs:subPropertyOf']['o'].keys():
                new['p']['rdfs:subPropertyOf']['o'][key] = set()
            lens1 = len(new['p']['rdfs:subPropertyOf']['s'][key])
            leno1 = len(new['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            new['p']['rdfs:subPropertyOf']['s'][key].add(key)
            new['p']['rdfs:subPropertyOf']['o'][key].add(key)
            lens2 = len(new['p']['rdfs:subPropertyOf']['s'][key])
            leno2 = len(new['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed

    def rdfs7_parentSubProperty(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:subPropertyOf" and self.s==other.p:
        #            result.add(other.s+" "+self.o+" "+other.o)
        #    return list(result)
        #    result = set()
        new = copy.deepcopy(current)

        changed = False

        sset = set(new['p']['rdfs:subPropertyOf']['s'].keys())
        pset = set(new['p'].keys())
        keys = sset.intersection(pset)
        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:subPropertyOf']['s'][key]:
                keypairs.add((key,o))

        for p,o in keypairs:
            if o not in new['p'].keys():
                new['p'][o] = {}
                new['p'][o]['s'] = {}
                new['p'][o]['o'] = {}
            for s in new['p'][p]['s'].keys():
                for o2 in new['p'][p]['s'][s]:
                    if s    not in new['p'][o]['s'].keys():
                        new['p'][o]['s'][s] = set()
                    if o2    not in new['p'][o]['o'].keys():
                        new['p'][o]['o'][o2] = set()
                    lens1 = len(new['p'][o]['s'][s])
                    leno1 = len(new['p'][o]['o'][o2])#This one is not needed I think...
                    new['p'][o]['s'][s].add(o2)
                    new['p'][o]['o'][o2].add(s)
                    lens2 = len(new['p'][o]['s'][s])
                    leno2 = len(new['p'][o]['o'][o2])#This one is not needed I think...
                    if (lens1!=lens2 or leno1!=leno2):
                        changed = True
        return new, changed

    def rdfs8_subClassResource(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdfs:Class":
        #    result.add(self.s+" rdfs:subClassOf rdfs:Resource")
        #return list(result)
        
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        if 'rdfs:Class' in new['p']['rdf:type']['o'].keys():
            for s in new['p']['rdf:type']['o']['rdfs:Class']:
                keys.add(s)
        else:
            return new, False

        for key in keys:
            if 'rdfs:subClassOf' not in new['p'].keys():
                new['p']['rdfs:subClassOf'] = {}
                new['p']['rdfs:subClassOf']['s'] = {}
                new['p']['rdfs:subClassOf']['o'] = {}
            if key              not in new['p']['rdfs:subClassOf']['s'].keys():
                new['p']['rdfs:subClassOf']['s'][key] = set()
            if 'rdfs:Resource'  not in new['p']['rdfs:subClassOf']['o'].keys():
                new['p']['rdfs:subClassOf']['o']['rdfs:Resource'] = set()
            lens1 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno1 = len(new['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            new['p']['rdfs:subClassOf']['s'][key].add('rdfs:Resource')
            new['p']['rdfs:subClassOf']['o']['rdfs:Resource'].add(key)
            lens2 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno2 = len(new['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed
    
    def rdfs9_typeOfClass(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subClassOf" and other.p=="rdf:type" and self.s==other.o:
        #        result.add(other.s+" rdf:type "+self.o)
        #return list(result)
        new = copy.deepcopy(current)

        changed = False

        sset = set(new['p']['rdfs:subClassOf']['s'].keys())
        oset = set(new['p']['rdf:type']['o'].keys())
        keys = sset.intersection(oset)

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        for key in keys:
            for o in new['p']['rdfs:subClassOf']['s'][key]:
                for s in new['p']['rdf:type']['o'][key]:
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
                    if (lens1!=lens2 or leno1!=leno2):
                        changed = True
        return new, changed

    def rdfs10_subClassSelf(self, current):
        #if self.p=="rdf:type" and self.o=="rdfs:Class:
        #    result.add(self.s+" rdfs:subClassOf "+self.s)
        #return list(result)
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        if 'rdfs:Class' in new['p']['rdf:type']['o'].keys():
            for s in new['p']['rdf:type']['o']['rdfs:Class']:
                keys.add(s)
        else:
            return new, False

        for key in keys:
            if 'rdfs:subClassOf' not in new['p'].keys():
                new['p']['rdfs:subClassOf'] = {}
                new['p']['rdfs:subClassOf']['s'] = {}
                new['p']['rdfs:subClassOf']['o'] = {}
            if key              not in new['p']['rdfs:subClassOf']['s'].keys():
                new['p']['rdfs:subClassOf']['s'][key] = set()
            if key  not in new['p']['rdfs:subClassOf']['o'].keys():
                new['p']['rdfs:subClassOf']['o'][key] = set()
            lens1 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno1 = len(new['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            new['p']['rdfs:subClassOf']['s'][key].add(key)
            new['p']['rdfs:subClassOf']['o'][key].add(key)
            lens2 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno2 = len(new['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed
    
    def rdfs11_subClass(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subClassOf" and other.p=="rdfs:subClassOf" and self.o==other.s:
        #        result.add(self.s+" rdfs:subClassOf "+other.o)
        #return list(result)
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        sset = set(new['p']['rdfs:subClassOf']['s'].keys())
        oset = set(new['p']['rdfs:subClassOf']['o'].keys())
        keys = sset.intersection(oset)

        for key in keys:
            for o in new['p']['rdfs:subClassOf']['s'][key]:
                for s in new['p']['rdfs:subClassOf']['o'][key]:
                    lens1 = len(new['p']['rdfs:subClassOf']['s'][s])
                    leno1 = len(new['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    new['p']['rdfs:subClassOf']['s'][s].add(o)
                    new['p']['rdfs:subClassOf']['o'][o].add(s)
                    lens2 = len(new['p']['rdfs:subClassOf']['s'][s])
                    leno2 = len(new['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    if (lens1!=lens2 or leno1!=leno2):
                        changed = True
        return new, changed    

    def rdfs12_container(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdfs:ContainerMembershipProperty":
        #    result.add(self.s+" rdfs:subPropertyOf rdfs:member")
        #return list(result)
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        if 'rdfs:ContainerMembershipProperty' in new['p']['rdf:type']['o'].keys():
            for s in new['p']['rdf:type']['o']['rdfs:ContainerMembershipProperty']:
                keys.add(s)
        else:
            return new, False


        for key in keys:
            if 'rdfs:subPropertyOf' not in new['p'].keys():
                new['p']['rdfs:subPropertyOf'] = {}
                new['p']['rdfs:subPropertyOf']['s'] = {}
                new['p']['rdfs:subPropertyOf']['o'] = {}
            if key              not in new['p']['rdfs:subPropertyOf']['s'].keys():
                new['p']['rdfs:subPropertyOf']['s'][key] = set()
            if 'rdfs:member'  not in new['p']['rdfs:subPropertyOf']['o'].keys():
                new['p']['rdfs:subPropertyOf']['o']['rdfs:member'] = set()
            lens1 = len(new['p']['rdfs:subPropertyOf']['s'][key])
            leno1 = len(new['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            new['p']['rdfs:subPropertyOf']['s'][key].add('rdfs:member')
            new['p']['rdfs:subPropertyOf']['o']['rdfs:member'].add(key)
            lens2 = len(new['p']['rdfs:subPropertyOf']['s'][key])
            leno2 = len(new['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed
    
    def rdfs13_literal(self, current):
        #    #result = set()
        #    #if self.p=="rdf:type" and self.o=="rdfs:Datatype":
        #    #    result.add(self.s+" rdfs:subClassOf rdfs:Literal")
        #    #return list(result)
        new = copy.deepcopy(current)

        changed = False

        keys = set()

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        if 'rdfs:Datatype' in new['p']['rdf:type']['o'].keys():
            for s in new['p']['rdf:type']['o']['rdfs:Datatype']:
                keys.add(s)
        else:
            return new, False


        for key in keys:
            if 'rdfs:subClassOf' not in new['p'].keys():
                new['p']['rdfs:subClassOf'] = {}
                new['p']['rdfs:subClassOf']['s'] = {}
                new['p']['rdfs:subClassOf']['o'] = {}
            if key              not in new['p']['rdfs:subClassOf']['s'].keys():
                new['p']['rdfs:subClassOf']['s'][key] = set()
            if 'rdfs:Literal'  not in new['p']['rdfs:subClassOf']['o'].keys():
                new['p']['rdfs:subClassOf']['o']['rdfs:Literal'] = set()
            lens1 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno1 = len(new['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            new['p']['rdfs:subClassOf']['s'][key].add('rdfs:Literal')
            new['p']['rdfs:subClassOf']['o']['rdfs:Literal'].add(key)
            lens2 = len(new['p']['rdfs:subClassOf']['s'][key])
            leno2 = len(new['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            if (lens1!=lens2 or leno1!=leno2):
                changed = True
        return new, changed

    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)
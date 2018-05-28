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
    
    def test_all_larger(self, current):
        new = copy.deepcopy(current)
        new, _non, rf1,     _nonb = (new, new, False, False)#self.rdfs1_allIsDataType(new)
        new, _non, rf2,     _nonb = self.rdfs2_domain(new)
        new, _non, rf3,     _nonb = self.rdfs3_range(new)
        new, _non, rf4a,    _nonb = self.rdfs4a_Resource(new)
        new, _non, rf4b,    _nonb = self.rdfs4b_Resource(new)
        new, _non, rf5,     _nonb = self.rdfs5_subProperty(new)
        new, _non, rf6,     _nonb = self.rdfs6_typeProperty(new)
        new, _non, rf7,     _nonb = self.rdfs7_parentSubProperty(new)
        new, _non, rf8,     _nonb = self.rdfs8_subClassResource(new)
        new, _non, rf9,     _nonb = self.rdfs9_typeOfClass(new)
        new, _non, rf10,    _nonb = self.rdfs10_subClassSelf(new)
        new, _non, rf11,    _nonb = self.rdfs11_subClass(new)
        new, _non, rf12,    _nonb = self.rdfs12_container(new)
        new, _non, rf13,    _nonb = self.rdfs13_literal(new)
        return new, (rf1 or rf2 or rf3 or rf4a or rf4b or rf5 or rf6 or rf7 or rf8 or rf9 or rf10 or rf11 or rf12 or rf13)

    def test_all_smaller(self, current):
        new = copy.deepcopy(current)
        _non, new, _nonb, rf1     = (new, new, False, False)#self.rdfs1_allIsDataType(new)
        _non, new, _nonb, rf2     = self.rdfs2_domain(new)
        _non, new, _nonb, rf3     = self.rdfs3_range(new)
        _non, new, _nonb, rf4a    = self.rdfs4a_Resource(new)
        _non, new, _nonb, rf4b    = self.rdfs4b_Resource(new)
        _non, new, _nonb, rf5     = self.rdfs5_subProperty(new)
        _non, new, _nonb, rf6     = self.rdfs6_typeProperty(new)
        _non, new, _nonb, rf7     = self.rdfs7_parentSubProperty(new)
        _non, new, _nonb, rf8     = self.rdfs8_subClassResource(new)
        _non, new, _nonb, rf9     = self.rdfs9_typeOfClass(new)
        _non, new, _nonb, rf10    = self.rdfs10_subClassSelf(new)
        _non, new, _nonb, rf11    = self.rdfs11_subClass(new)
        _non, new, _nonb, rf12    = self.rdfs12_container(new)
        _non, new, _nonb, rf13    = self.rdfs13_literal(new)
        return new, (rf1 or rf2 or rf3 or rf4a or rf4b or rf5 or rf6 or rf7 or rf8 or rf9 or rf10 or rf11 or rf12 or rf13)

    '''def subd_singleRules(self, current):
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
        return new, (rf1 or rf4a or rf4b or rf6 or rf8 or rf10 or rf12 or rf13)'''

    def lsubs_dora(self, current):
        new = copy.deepcopy(current)
        new, _s, rf2, _b, = self.rdfs2_domain(new)
        new, _s, rf3, _b = self.rdfs3_range(new)
        return new, (rf2 or rf3)

    def lsubs_heritage(self, current):
        new = copy.deepcopy(current)
        rf7 = False
        rf9 = False
        new, _s, rf7, _b = self.rdfs7_parentSubProperty(new)
        new, _s, rf9, _b = self.rdfs9_typeOfClass(new)
        return new, (rf7 or rf9)

    def lsubs_subSome(self, current):
        new = copy.deepcopy(current)
        new, _s, rf5, _b = self.rdfs5_subProperty(new)
        new, _s, rf11, _b = self.rdfs11_subClass(new)
        return new, (rf5 or rf11)

    def ssubs_dora(self, current):
        new = copy.deepcopy(current)
        _s, new, _b, rf2 = self.rdfs2_domain(new)
        _s, new, _b, rf3 = self.rdfs3_range(new)
        return new, (rf2 or rf3)

    def ssubs_heritage(self, current):
        new = copy.deepcopy(current)
        rf7 = False
        rf9 = False
        _s, new, _b, rf7 = self.rdfs7_parentSubProperty(new)
        _s, new, _b, rf9 = self.rdfs9_typeOfClass(new)
        return new, (rf7 or rf9)

    def ssubs_subSome(self, current):
        new = copy.deepcopy(current)
        _s, new, _b, rf5 = self.rdfs5_subProperty(new)
        _s, new, _b, rf11 = self.rdfs11_subClass(new)
        return new, (rf5 or rf11)

    def rdfs1_allIsDataType(self, current):
        new = copy.deepcopy(current)

        keys = set()

        lchanged = False
        schanged = False

        for p in new['p'].keys():
            keys.add(p)
            for s in new['p'][p]['s'].keys():
                keys.add(s)
                for o in new['p'][p]['s'][s]:
                    keys.add(o)

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdf:type' not in larger['p'].keys():
                larger['p']['rdf:type'] = {}
                larger['p']['rdf:type']['s'] = {}
                larger['p']['rdf:type']['o'] = {}
                smaller['p']['rdf:type'] = {}
                smaller['p']['rdf:type']['s'] = {}
                smaller['p']['rdf:type']['o'] = {}
            if key              not in larger['p']['rdf:type']['s'].keys():
                larger['p']['rdf:type']['s'][key] = set()
                smaller['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Datatype'  not in larger['p']['rdf:type']['o'].keys():
                larger['p']['rdf:type']['o']['rdfs:Datatype'] = set()
                smaller['p']['rdf:type']['o']['rdfs:Datatype'] = set()
            llens1 = len(larger['p']['rdf:type']['s'][key])
            lleno1 = len(larger['p']['rdf:type']['o']['rdfs:Datatype'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdf:type']['s'][key])
            sleno1 = len(smaller['p']['rdf:type']['o']['rdfs:Datatype'])#This one is not needed I think...
            larger['p']['rdf:type']['s'][key].add('rdfs:Datatype')
            larger['p']['rdf:type']['o']['rdfs:Datatype'].add(key)
            try:
                smaller['p']['rdf:type']['s'][key].remove('rdfs:Datatype')
                smaller['p']['rdf:type']['o']['rdfs:Datatype'].remove(key)
            except KeyError:
                print("No Key") 
            llens2 = len(larger['p']['rdf:type']['s'][key])
            lleno2 = len(larger['p']['rdf:type']['o']['rdfs:Datatype'])#This one is not needed I think...
            slens2 = len(smaller['p']['rdf:type']['s'][key])
            sleno2 = len(smaller['p']['rdf:type']['o']['rdfs:Datatype'])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs2_domain(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:domain" and self.s==other.p:
        #            result.add(other.s+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        if 'rdfs:domain' in new['p'].keys():
            sset = set(new['p']['rdfs:domain']['s'].keys())
            pset = set(new['p'].keys())
            keys = sset.intersection(pset)
            keypairs = set()

            for key in keys:
                for o in new['p']['rdfs:domain']['s'][key]:
                    keypairs.add((key,o))

            larger = copy.deepcopy(new)
            smaller = copy.deepcopy(new)
            for p,o in keypairs:
                if 'rdf:type' not in larger['p'].keys():
                    larger['p']['rdf:type'] = {}
                    larger['p']['rdf:type']['s'] = {}
                    larger['p']['rdf:type']['o'] = {}
                    smaller['p']['rdf:type'] = {}
                    smaller['p']['rdf:type']['s'] = {}
                    smaller['p']['rdf:type']['o'] = {}
                for s in larger['p'][p]['s'].keys():
                    if s    not in larger['p']['rdf:type']['s'].keys():
                        larger['p']['rdf:type']['s'][s] = set()
                        smaller['p']['rdf:type']['s'][s] = set()
                    if o    not in larger['p']['rdf:type']['o'].keys():
                        larger['p']['rdf:type']['o'][o] = set()
                        smaller['p']['rdf:type']['o'][o] = set()
                    llens1 = len(larger['p']['rdf:type']['s'][s])
                    lleno1 = len(larger['p']['rdf:type']['o'][o])#This one is not needed I think...
                    slens1 = len(smaller['p']['rdf:type']['s'][s])
                    sleno1 = len(smaller['p']['rdf:type']['o'][o])#This one is not needed I think...
                    larger['p']['rdf:type']['s'][s].add(o)
                    larger['p']['rdf:type']['o'][o].add(s)
                    try:
                        smaller['p']['rdf:type']['s'][s].remove(o)
                        smaller['p']['rdf:type']['o'][o].remove(s)
                    except KeyError:
                        print("No Key")
                    llens2 = len(larger['p']['rdf:type']['s'][s])
                    lleno2 = len(larger['p']['rdf:type']['o'][o])#This one is not needed I think...
                    slens2 = len(smaller['p']['rdf:type']['s'][s])
                    sleno2 = len(smaller['p']['rdf:type']['o'][o])#This one is not needed I think...
                    if (llens1!=llens2 or lleno1!=lleno2):
                        lchanged = True
                    if (slens1!=slens2 or sleno1!=sleno2):
                        schanged = True
            return larger, smaller, lchanged, schanged,
        else:
            return new, new, False, False

    def rdfs3_range(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:range" and self.s==other.p:
        #            result.add(other.o+" rdf:type "+self.o)
        #    return list(result)'''
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        if 'rdfs:range' not in new['p'].keys():
            new['p']['rdfs:range'] = {}
            new['p']['rdfs:range']['s'] = {}
            new['p']['rdfs:range']['o'] = {}

        try:
            sset = set(new['p']['rdfs:range']['s'].keys())
            pset = set(new['p'].keys())
            keys = sset.intersection(pset)
        except KeyError:
            return new, new, False, False

        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:range']['s'][key]:
                keypairs.add((key,o))

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for p,o in keypairs:
            if 'rdf:type' not in larger['p'].keys():
                larger['p']['rdf:type'] = {}
                larger['p']['rdf:type']['s'] = {}
                larger['p']['rdf:type']['o'] = {}
                smaller['p']['rdf:type'] = {}
                smaller['p']['rdf:type']['s'] = {}
                smaller['p']['rdf:type']['o'] = {}
            for o2 in new['p'][p]['o'].keys():
                if o2    not in larger['p']['rdf:type']['s'].keys():
                    larger['p']['rdf:type']['s'][o2] = set()
                    smaller['p']['rdf:type']['s'][o2] = set()
                if o    not in larger['p']['rdf:type']['o'].keys():
                    larger['p']['rdf:type']['o'][o] = set()
                    smaller['p']['rdf:type']['o'][o] = set()
                llens1 = len(larger['p']['rdf:type']['s'][o2])
                lleno1 = len(larger['p']['rdf:type']['o'][o])#This one is not needed I think...
                slens1 = len(smaller['p']['rdf:type']['s'][o2])
                sleno1 = len(smaller['p']['rdf:type']['o'][o])#This one is not needed I think...
                larger['p']['rdf:type']['s'][o2].add(o)
                larger['p']['rdf:type']['o'][o].add(o2)
                try:
                    smaller['p']['rdf:type']['s'][o2].remove(o)
                    smaller['p']['rdf:type']['o'][o].remove(o2)
                except KeyError:
                    print("No Key")
                llens2 = len(larger['p']['rdf:type']['s'][o2])
                lleno2 = len(larger['p']['rdf:type']['o'][o])
                slens2 = len(smaller['p']['rdf:type']['s'][o2])
                sleno2 = len(smaller['p']['rdf:type']['o'][o])
                if (llens1!=llens2 or lleno1!=lleno2):
                    lchanged = True
                if (slens1!=slens2 or sleno1!=sleno2):
                    schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs4a_Resource(self, current):
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        keys = set()

        for p in new['p'].keys():
            for s in new['p'][p]['s'].keys():
                keys.add(s)

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdf:type' not in larger['p'].keys():
                larger['p']['rdf:type'] = {}
                larger['p']['rdf:type']['s'] = {}
                larger['p']['rdf:type']['o'] = {}
                smaller['p']['rdf:type'] = {}
                smaller['p']['rdf:type']['s'] = {}
                smaller['p']['rdf:type']['o'] = {}
            if key              not in larger['p']['rdf:type']['s'].keys():
                larger['p']['rdf:type']['s'][key] = set()
                smaller['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Resource'  not in larger['p']['rdf:type']['o'].keys():
                larger['p']['rdf:type']['o']['rdfs:Resource'] = set()
                smaller['p']['rdf:type']['o']['rdfs:Resource'] = set()
            llens1 = len(larger['p']['rdf:type']['s'][key])
            lleno1 = len(larger['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdf:type']['s'][key])
            sleno1 = len(smaller['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            larger['p']['rdf:type']['s'][key].add('rdfs:Resource')
            larger['p']['rdf:type']['o']['rdfs:Resource'].add(key)
            try:
                smaller['p']['rdf:type']['s'][key].remove('rdfs:Resource')
                smaller['p']['rdf:type']['o']['rdfs:Resource'].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdf:type']['s'][key])
            lleno2 = len(larger['p']['rdf:type']['o']['rdfs:Resource'])
            slens2 = len(smaller['p']['rdf:type']['s'][key])
            sleno2 = len(smaller['p']['rdf:type']['o']['rdfs:Resource'])
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs4b_Resource(self, current):
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        keys = set()

        for p in new['p'].keys():
            for o in new['p'][p]['o'].keys():
                keys.add(o)

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdf:type' not in larger['p'].keys():
                larger['p']['rdf:type'] = {}
                larger['p']['rdf:type']['s'] = {}
                larger['p']['rdf:type']['o'] = {}
                smaller['p']['rdf:type'] = {}
                smaller['p']['rdf:type']['s'] = {}
                smaller['p']['rdf:type']['o'] = {}
            if key              not in larger['p']['rdf:type']['s'].keys():
                larger['p']['rdf:type']['s'][key] = set()
                smaller['p']['rdf:type']['s'][key] = set()
            if 'rdfs:Resource'  not in larger['p']['rdf:type']['o'].keys():
                larger['p']['rdf:type']['o']['rdfs:Resource'] = set()
                smaller['p']['rdf:type']['o']['rdfs:Resource'] = set()
            llens1 = len(larger['p']['rdf:type']['s'][key])
            lleno1 = len(larger['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdf:type']['s'][key])
            sleno1 = len(smaller['p']['rdf:type']['o']['rdfs:Resource'])#This one is not needed I think...
            larger['p']['rdf:type']['s'][key].add('rdfs:Resource')
            larger['p']['rdf:type']['o']['rdfs:Resource'].add(key)
            try:
                smaller['p']['rdf:type']['s'][key].remove('rdfs:Resource')
                smaller['p']['rdf:type']['o']['rdfs:Resource'].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdf:type']['s'][key])
            lleno2 = len(larger['p']['rdf:type']['o']['rdfs:Resource'])
            slens2 = len(smaller['p']['rdf:type']['s'][key])
            sleno2 = len(smaller['p']['rdf:type']['o']['rdfs:Resource'])
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs5_subProperty(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subPropertyOf" and other.p=="rdfs:subPropertyOf" and self.s==other.o:
        #        result.add(self.s+" rdfs:subPropertyOf "+other.o)
        #return list(result)'''

        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        keys = set()

        try:
            sset = set(new['p']['rdfs:subPropertyOf']['s'].keys())
            oset = set(new['p']['rdfs:subPropertyOf']['o'].keys())
            keys = sset.intersection(oset)
        except KeyError:
            return new, new, False, False

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            for o in new['p']['rdfs:subPropertyOf']['s'][key]:
                for s in new['p']['rdfs:subPropertyOf']['o'][key]:
                    llens1 = len(larger['p']['rdfs:subPropertyOf']['s'][s])
                    lleno1 = len(larger['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    slens1 = len(smaller['p']['rdfs:subPropertyOf']['s'][s])
                    sleno1 = len(smaller['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    larger['p']['rdfs:subPropertyOf']['s'][s].add(o)
                    larger['p']['rdfs:subPropertyOf']['o'][o].add(s)
                    try:
                        smaller['p']['rdfs:subPropertyOf']['s'][s].remove(o)
                        smaller['p']['rdfs:subPropertyOf']['o'][o].remove(s)
                    except KeyError:
                        print("No Key")
                    llens2 = len(larger['p']['rdfs:subPropertyOf']['s'][s])
                    lleno2 = len(larger['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    slens2 = len(smaller['p']['rdfs:subPropertyOf']['s'][s])
                    sleno2 = len(smaller['p']['rdfs:subPropertyOf']['o'][o])#This one is not needed I think...
                    if (llens1!=llens2 or lleno1!=lleno2):
                        lchanged = True
                    if (slens1!=slens2 or sleno1!=sleno2):
                        schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs6_typeProperty(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdf:Property":
        #    result.add(self.s+" rdfs:subPropertyOf "+self.s)
        #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

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

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdfs:subPropertyOf' not in larger['p'].keys():
                larger['p']['rdfs:subPropertyOf'] = {}
                larger['p']['rdfs:subPropertyOf']['s'] = {}
                larger['p']['rdfs:subPropertyOf']['o'] = {}
                smaller['p']['rdfs:subPropertyOf'] = {}
                smaller['p']['rdfs:subPropertyOf']['s'] = {}
                smaller['p']['rdfs:subPropertyOf']['o'] = {}
            if key  not in larger['p']['rdfs:subPropertyOf']['s'].keys():
                larger['p']['rdfs:subPropertyOf']['s'][key] = set()
                smaller['p']['rdfs:subPropertyOf']['s'][key] = set()
            if key  not in larger['p']['rdfs:subPropertyOf']['o'].keys():
                larger['p']['rdfs:subPropertyOf']['o'][key] = set()
                smaller['p']['rdfs:subPropertyOf']['o'][key] = set()
            llens1 = len(larger['p']['rdfs:subPropertyOf']['s'][key])
            lleno1 = len(larger['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            slens1 = len(smaller['p']['rdfs:subPropertyOf']['s'][key])
            sleno1 = len(smaller['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            larger['p']['rdfs:subPropertyOf']['s'][key].add(key)
            larger['p']['rdfs:subPropertyOf']['o'][key].add(key)
            try:
                smaller['p']['rdfs:subPropertyOf']['s'][key].remove(key)
                smaller['p']['rdfs:subPropertyOf']['o'][key].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdfs:subPropertyOf']['s'][key])
            lleno2 = len(larger['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            slens2 = len(smaller['p']['rdfs:subPropertyOf']['s'][key])
            sleno2 = len(smaller['p']['rdfs:subPropertyOf']['o'][key])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs7_parentSubProperty(self, current):
        #    result = set()
        #    for other in store:
        #        if self.p=="rdfs:subPropertyOf" and self.s==other.p:
        #            result.add(other.s+" "+self.o+" "+other.o)
        #    return list(result)
        #    result = set()
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        try:
            sset = set(new['p']['rdfs:subPropertyOf']['s'].keys())
            pset = set(new['p'].keys())
            keys = sset.intersection(pset)
        except KeyError:
            return new, new, False, False

        keypairs = set()

        for key in keys:
            for o in new['p']['rdfs:subPropertyOf']['s'][key]:
                keypairs.add((key,o))

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for p,o in keypairs:
            if o not in larger['p'].keys():
                larger['p'][o] = {}
                larger['p'][o]['s'] = {}
                larger['p'][o]['o'] = {}
                smaller['p'][o] = {}
                smaller['p'][o]['s'] = {}
                smaller['p'][o]['o'] = {}
            for s in larger['p'][p]['s'].keys():
                for o2 in larger['p'][p]['s'][s]:
                    if s    not in larger['p'][o]['s'].keys():
                        larger['p'][o]['s'][s] = set()
                        smaller['p'][o]['s'][s] = set()
                    if o2    not in larger['p'][o]['o'].keys():
                        larger['p'][o]['o'][o2] = set()
                        smaller['p'][o]['o'][o2] = set()
                    llens1 = len(larger['p'][o]['s'][s])
                    lleno1 = len(larger['p'][o]['o'][o2])#This one is not needed I think...
                    slens1 = len(smaller['p'][o]['s'][s])
                    sleno1 = len(smaller['p'][o]['o'][o2])#This one is not needed I think...
                    larger['p'][o]['s'][s].add(o2)
                    larger['p'][o]['o'][o2].add(s)
                    try:
                        smaller['p'][o]['s'][s].remove(o2)
                        smaller['p'][o]['o'][o2].remove(s)
                    except KeyError:
                        print("No Key")
                    llens2 = len(larger['p'][o]['s'][s])
                    lleno2 = len(larger['p'][o]['o'][o2])#This one is not needed I think...
                    slens2 = len(smaller['p'][o]['s'][s])
                    sleno2 = len(smaller['p'][o]['o'][o2])#This one is not needed I think...
                    if (llens1!=llens2 or lleno1!=lleno2):
                        lchanged = True
                    if (slens1!=slens2 or sleno1!=sleno2):
                        schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs8_subClassResource(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdfs:Class":
        #    result.add(self.s+" rdfs:subClassOf rdfs:Resource")
        #return list(result)

        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

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

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdfs:subClassOf' not in larger['p'].keys():
                larger['p']['rdfs:subClassOf'] = {}
                larger['p']['rdfs:subClassOf']['s'] = {}
                larger['p']['rdfs:subClassOf']['o'] = {}
                smaller['p']['rdfs:subClassOf'] = {}
                smaller['p']['rdfs:subClassOf']['s'] = {}
                smaller['p']['rdfs:subClassOf']['o'] = {}
            if key              not in larger['p']['rdfs:subClassOf']['s'].keys():
                larger['p']['rdfs:subClassOf']['s'][key] = set()
                smaller['p']['rdfs:subClassOf']['s'][key] = set()
            if 'rdfs:Resource'  not in larger['p']['rdfs:subClassOf']['o'].keys():
                larger['p']['rdfs:subClassOf']['o']['rdfs:Resource'] = set()
                smaller['p']['rdfs:subClassOf']['o']['rdfs:Resource'] = set()
            llens1 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno1 = len(larger['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno1 = len(smaller['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            larger['p']['rdfs:subClassOf']['s'][key].add('rdfs:Resource')
            larger['p']['rdfs:subClassOf']['o']['rdfs:Resource'].add(key)
            try:
                smaller['p']['rdfs:subClassOf']['s'][key].remove('rdfs:Resource')
                smaller['p']['rdfs:subClassOf']['o']['rdfs:Resource'].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno2 = len(larger['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            slens2 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno2 = len(smaller['p']['rdfs:subClassOf']['o']['rdfs:Resource'])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs9_typeOfClass(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subClassOf" and other.p=="rdf:type" and self.s==other.o:
        #        result.add(other.s+" rdf:type "+self.o)
        #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        try:
            sset = set(new['p']['rdfs:subClassOf']['s'].keys())
            oset = set(new['p']['rdf:type']['o'].keys())
            keys = sset.intersection(oset)
        except KeyError:
            return new, new, False, False

        if 'rdf:type' not in new['p'].keys():
            new['p']['rdf:type'] = {}
            new['p']['rdf:type']['s'] = {}
            new['p']['rdf:type']['o'] = {}
        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            for o in larger['p']['rdfs:subClassOf']['s'][key]:
                for s in larger['p']['rdf:type']['o'][key]:
                    if s    not in larger['p']['rdf:type']['s'].keys():
                        larger['p']['rdf:type']['s'][s] = set()
                        smaller['p']['rdf:type']['s'][s] = set()
                    if o    not in larger['p']['rdf:type']['o'].keys():
                        larger['p']['rdf:type']['o'][o] = set()
                        smaller['p']['rdf:type']['o'][o] = set()
                    llens1 = len(larger['p']['rdf:type']['s'][s])
                    lleno1 = len(larger['p']['rdf:type']['o'][o])#This one is not needed I think...
                    slens1 = len(smaller['p']['rdf:type']['s'][s])
                    sleno1 = len(smaller['p']['rdf:type']['o'][o])#This one is not needed I think...
                    larger['p']['rdf:type']['s'][s].add(o)
                    larger['p']['rdf:type']['o'][o].add(s)
                    try:
                        smaller['p']['rdf:type']['s'][s].remove(o)
                        smaller['p']['rdf:type']['o'][o].remove(s)
                    except KeyError:
                        print("No Key")
                    llens2 = len(larger['p']['rdf:type']['s'][s])
                    lleno2 = len(larger['p']['rdf:type']['o'][o])
                    slens2 = len(smaller['p']['rdf:type']['s'][s])
                    sleno2 = len(smaller['p']['rdf:type']['o'][o])
                    if (llens1!=llens2 or lleno1!=lleno2):
                        lchanged = True
                    if (slens1!=slens2 or sleno1!=sleno2):
                        schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs10_subClassSelf(self, current):
        #if self.p=="rdf:type" and self.o=="rdfs:Class:
        #    result.add(self.s+" rdfs:subClassOf "+self.s)
        #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

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

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdfs:subClassOf' not in larger['p'].keys():
                larger['p']['rdfs:subClassOf'] = {}
                larger['p']['rdfs:subClassOf']['s'] = {}
                larger['p']['rdfs:subClassOf']['o'] = {}
                smaller['p']['rdfs:subClassOf'] = {}
                smaller['p']['rdfs:subClassOf']['s'] = {}
                smaller['p']['rdfs:subClassOf']['o'] = {}
            if key              not in larger['p']['rdfs:subClassOf']['s'].keys():
                larger['p']['rdfs:subClassOf']['s'][key] = set()
                smaller['p']['rdfs:subClassOf']['s'][key] = set()
            if key  not in larger['p']['rdfs:subClassOf']['o'].keys():
                larger['p']['rdfs:subClassOf']['o'][key] = set()
                smaller['p']['rdfs:subClassOf']['o'][key] = set()
            llens1 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno1 = len(larger['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            slens1 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno1 = len(smaller['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            larger['p']['rdfs:subClassOf']['s'][key].add(key)
            larger['p']['rdfs:subClassOf']['o'][key].add(key)
            try:
                smaller['p']['rdfs:subClassOf']['s'][key].remove(key)
                smaller['p']['rdfs:subClassOf']['o'][key].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno2 = len(larger['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            slens2 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno2 = len(smaller['p']['rdfs:subClassOf']['o'][key])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs11_subClass(self, current):
        #result = set()
        #for other in store:
        #    if self.p=="rdfs:subClassOf" and other.p=="rdfs:subClassOf" and self.o==other.s:
        #        result.add(self.s+" rdfs:subClassOf "+other.o)
        #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

        keys = set()

        try:
            sset = set(new['p']['rdfs:subClassOf']['s'].keys())
            oset = set(new['p']['rdfs:subClassOf']['o'].keys())
            keys = sset.intersection(oset)
        except KeyError:
            return new, new, False, False

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            for o in new['p']['rdfs:subClassOf']['s'][key]:
                for s in new['p']['rdfs:subClassOf']['o'][key]:
                    llens1 = len(larger['p']['rdfs:subClassOf']['s'][s])
                    lleno1 = len(larger['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    slens1 = len(smaller['p']['rdfs:subClassOf']['s'][s])
                    sleno1 = len(smaller['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    larger['p']['rdfs:subClassOf']['s'][s].add(o)
                    larger['p']['rdfs:subClassOf']['o'][o].add(s)
                    try:
                        smaller['p']['rdfs:subClassOf']['s'][s].remove(o)
                        smaller['p']['rdfs:subClassOf']['o'][o].remove(s)
                    except KeyError:
                        print("No Key")
                    llens2 = len(larger['p']['rdfs:subClassOf']['s'][s])
                    lleno2 = len(larger['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    slens2 = len(smaller['p']['rdfs:subClassOf']['s'][s])
                    sleno2 = len(smaller['p']['rdfs:subClassOf']['o'][o])#This one is not needed I think...
                    if (llens1!=llens2 or lleno1!=lleno2):
                        lchanged = True
                    if (slens1!=slens2 or sleno1!=sleno2):
                        schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs12_container(self, current):
        #result = set()
        #if self.p=="rdf:type" and self.o=="rdfs:ContainerMembershipProperty":
        #    result.add(self.s+" rdfs:subPropertyOf rdfs:member")
        #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

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


        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if 'rdfs:subPropertyOf' not in larger['p'].keys():
                larger['p']['rdfs:subPropertyOf'] = {}
                larger['p']['rdfs:subPropertyOf']['s'] = {}
                larger['p']['rdfs:subPropertyOf']['o'] = {}
                smaller['p']['rdfs:subPropertyOf'] = {}
                smaller['p']['rdfs:subPropertyOf']['s'] = {}
                smaller['p']['rdfs:subPropertyOf']['o'] = {}
            if key              not in larger['p']['rdfs:subPropertyOf']['s'].keys():
                larger['p']['rdfs:subPropertyOf']['s'][key] = set()
                smaller['p']['rdfs:subPropertyOf']['s'][key] = set()
            if 'rdfs:member'  not in larger['p']['rdfs:subPropertyOf']['o'].keys():
                larger['p']['rdfs:subPropertyOf']['o']['rdfs:member'] = set()
                smaller['p']['rdfs:subPropertyOf']['o']['rdfs:member'] = set()
            llens1 = len(larger['p']['rdfs:subPropertyOf']['s'][key])
            lleno1 = len(larger['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdfs:subPropertyOf']['s'][key])
            sleno1 = len(smaller['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            larger['p']['rdfs:subPropertyOf']['s'][key].add('rdfs:member')
            larger['p']['rdfs:subPropertyOf']['o']['rdfs:member'].add(key)
            try:
                smaller['p']['rdfs:subPropertyOf']['s'][key].remove('rdfs:member')
                smaller['p']['rdfs:subPropertyOf']['o']['rdfs:member'].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdfs:subPropertyOf']['s'][key])
            lleno2 = len(larger['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            slens2 = len(smaller['p']['rdfs:subPropertyOf']['s'][key])
            sleno2 = len(smaller['p']['rdfs:subPropertyOf']['o']['rdfs:member'])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def rdfs13_literal(self, current):
        #    #result = set()
        #    #if self.p=="rdf:type" and self.o=="rdfs:Datatype":
        #    #    result.add(self.s+" rdfs:subClassOf rdfs:Literal")
        #    #return list(result)
        new = copy.deepcopy(current)

        lchanged = False
        schanged = False

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

        if 'rdfs:subClassOf' not in new['p'].keys():
            new['p']['rdfs:subClassOf'] = {}
            new['p']['rdfs:subClassOf']['s'] = {}
            new['p']['rdfs:subClassOf']['o'] = {}

        larger = copy.deepcopy(new)
        smaller = copy.deepcopy(new)
        for key in keys:
            if key not in larger['p']['rdfs:subClassOf']['s'].keys():
                larger['p']['rdfs:subClassOf']['s'][key] = set()
                smaller['p']['rdfs:subClassOf']['s'][key] = set()
            if 'rdfs:Literal'  not in larger['p']['rdfs:subClassOf']['o'].keys():
                larger['p']['rdfs:subClassOf']['o']['rdfs:Literal'] = set()
                smaller['p']['rdfs:subClassOf']['o']['rdfs:Literal'] = set()
            
            llens1 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno1 = len(larger['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            slens1 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno1 = len(smaller['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            larger['p']['rdfs:subClassOf']['s'][key].add('rdfs:Literal')
            larger['p']['rdfs:subClassOf']['o']['rdfs:Literal'].add(key)
            try:
                smaller['p']['rdfs:subClassOf']['s'][key].remove('rdfs:Literal')
                smaller['p']['rdfs:subClassOf']['o']['rdfs:Literal'].remove(key)
            except KeyError:
                print("No Key")
            llens2 = len(larger['p']['rdfs:subClassOf']['s'][key])
            lleno2 = len(larger['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            slens2 = len(smaller['p']['rdfs:subClassOf']['s'][key])
            sleno2 = len(smaller['p']['rdfs:subClassOf']['o']['rdfs:Literal'])#This one is not needed I think...
            if (llens1!=llens2 or lleno1!=lleno2):
                lchanged = True
            if (slens1!=slens2 or sleno1!=sleno2):
                schanged = True
        return larger, smaller, lchanged, schanged,

    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)

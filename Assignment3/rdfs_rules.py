class rdfs_rules(object):
    s = ""
    p = ""
    o = ""
    pair = ""

    def __init__(self, pair):
        self.s = pair[0]
        self.p = pair[1]
        self.o = pair[2]
        self.pair = pair
    
    def rdfs1_allIsDataType(self, store):
        result = set()
        result.add(self.s+" rdf:type rdfs:Datatype")
        result.add(self.p+" rdf:type rdfs:Datatype")
        result.add(self.o+" rdf:type rdfs:Datatype")
        return list(result)

    def rdfs2_domain(self, store):
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
    #    result.add(self.s+" rdf:type rdfs:Datatype")
    #    return list(result)

    #def rdfs4b_Resource(self, store):
    #    result = set()
    #    result.add(self.o+" rdf:type rdfs:Datatype")
    #    return list(result) #Hoe is dit anders dan 1?

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
        return (self.p==other.p and self.o==other.o and self.s==other.s)


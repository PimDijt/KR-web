class ruler(object):
    s = ""
    p = ""
    o = ""
    pair = ""

    def __init__(self, pair):
        self.s = pair[0]
        self.p = pair[1]
        self.o = pair[2]
        self.pair = pair
    
    '''def rdfs1_allIsDataType(self, store):
        result = set()
        result.add(self.s+" a rdfs:Datatype")
        result.add(self.p+" a rdfs:Datatype")
        result.add(self.o+" a rdfs:Datatype")
        return list(result)'''

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
    #            result.add(other.o+" a "+self.o)
    #    return list(result)

    '''def rdfs4a_Resource(self, store):
        result = set()
        result.add(self.s+" a rdfs:Datatype")
        return list(result)

    def rdfs4b_Resource(self, store):
        result = set()
        result.add(self.s+" a rdfs:Datatype")
        return list(result)'''

    '''def rdfs5_range(self, store):
        result = set()
        for other in store:
            if self.p=="rdfs:subPropertyOf" and other.p=="rdfs:subPropertyOf" and self.s==other.o:
                result.add(self.s+" rdfs:subPropertyOf "+other.o)
        return list(result)

    def rdfs6_Property(self, store):
        result = set()
        if self.p=="a" and self.o=="rdf:Property":
            result.add(self.s+" rdfs:subPropertyOf "+self.s)
        return list(result)'''

    '''
            
            
            If S contains: 	then S RDFS entails recognizing D:
    rdfs1 	any IRI aaa in D 	aaa rdf:type rdfs:Datatype .
    rdfs2 	aaa rdfs:domain xxx .
    yyy aaa zzz . 	yyy rdf:type xxx .
    rdfs3 	aaa rdfs:range xxx .
    yyy aaa zzz . 	zzz rdf:type xxx .
    rdfs4a 	xxx aaa yyy . 	xxx rdf:type rdfs:Resource .
    rdfs4b 	xxx aaa yyy. 	yyy rdf:type rdfs:Resource .
    rdfs5 	xxx rdfs:subPropertyOf yyy .
    yyy rdfs:subPropertyOf zzz . 	xxx rdfs:subPropertyOf zzz .
    rdfs6 	xxx rdf:type rdf:Property . 	xxx rdfs:subPropertyOf xxx .
    rdfs7 	aaa rdfs:subPropertyOf bbb .
    xxx aaa yyy . 	xxx bbb yyy .
    rdfs8 	xxx rdf:type rdfs:Class . 	xxx rdfs:subClassOf rdfs:Resource .
    rdfs9 	xxx rdfs:subClassOf yyy .
    zzz rdf:type xxx . 	zzz rdf:type yyy .
    rdfs10 	xxx rdf:type rdfs:Class . 	xxx rdfs:subClassOf xxx .
    rdfs11 	xxx rdfs:subClassOf yyy .
    yyy rdfs:subClassOf zzz . 	xxx rdfs:subClassOf zzz .
    rdfs12 	xxx rdf:type rdfs:ContainerMembershipProperty . 	xxx rdfs:subPropertyOf rdfs:member .
    rdfs13 	xxx rdf:type rdfs:Datatype . 	xxx rdfs:subClassOf rdfs:Literal .'''

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
    
    def rdfs12_container(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdfs:ContainerMembershipProperty":
            result.add(self.s+" rdfs:subPropertyOf rdfs:member")
        return list(result)
    
    def rdfs13_literal(self, store):
        result = set()
        if self.p=="rdf:type" and self.o=="rdfs:Datatype":
            result.add(self.s+" rdfs:subClassOf rdfs:Literal")
        return list(result)
    
    def rdfs_bonus1(self, store):
        result = set()
        if self.p=="a":
            result.add(self.s+" rdf:type "+self.o)
        return list(result)

    def rdfs_bonus2(self, store):
        result = set()
        if self.p=="sc":
            result.add(self.s+" rdfs:subClassOf "+self.o)
        return list(result)

    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)


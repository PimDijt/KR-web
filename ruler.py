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

    def rdfs9_classOf(self, store):
        result = set()
        for other in store:
            if other.p=="sc" and self.p=="a" and self.o==other.s:
                result.add(self.s+" "+self.p+" "+other.o)
        return list(result)

    def rdfs11_classrel(self, store):
        result = set()
        for other in store:
            if other.p=="sc" and self.p=="sc" and self.o==other.s:
                result.add(self.s+" "+self.p+" "+other.o)
        return list(result)
    
    def equals(self, other):
        #print(self.s,other.s)
        #print(self.p,other.p)
        #print(self.o,other.o)
        return (self.p==other.p and self.o==other.o and self.s==other.s)


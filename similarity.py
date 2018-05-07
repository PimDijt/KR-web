import pickle
import Levenshtein
import fuzzy
import re

with open('dbo_label_dict.pickle', 'rb') as f:
    dbo_label_dict = pickle.load(f)

with open('dbtune_label_dict.pickle', 'rb') as f:
    dbtune_label_dict = pickle.load(f)

dmeta = fuzzy.DMetaphone()

str_count = 0
str_intersect_count = 0

dmeta_count = 0
dmeta_intersect_count = 0

nysiss_count = 0
nysiss_intersect_count = 0

for k, v in dbtune_label_dict.items():
    v = ''.join(e for e in v if e.isalnum() or e == " ")
    v_dmeta = dmeta(v.encode('utf-8'))[0]
    if v_dmeta != None:
        v_dmeta = bytes.decode(v_dmeta)
    v_nysiss = fuzzy.nysiis(v)
    str_found = False
    dmeta_found = False
    nysiss_found = False
    for k2, v2 in dbo_label_dict.items():
        v2 = ''.join(e for e in v2 if e.isalnum() or e == " ")
        v2_dmeta = dmeta(v2.encode('utf-8'))[0]
        v2_nysiss = fuzzy.nysiis(v2)
        #first do String
        dist = Levenshtein.distance(v, v2)
        longest = len(v) if len(v)>len(v2) else len(v2)
        if longest != 0:
            if dist/longest < 0.1:
                print(v+"-"+v2)
                str_count += 1
                if not str_found:
                    str_found = True
                    str_intersect_count += 1
        #then do dmeta
        if v_dmeta != None and v2_dmeta != None:
            v2_dmeta = bytes.decode(v2_dmeta)
            dist = Levenshtein.distance(v_dmeta, v2_dmeta)
            longest = len(v_dmeta) if len(v_dmeta)>len(v2_dmeta) else len(v2_dmeta)
            if longest != 0:
                if dist/longest < 0.1:
                    print(v_dmeta+"-"+v2_dmeta)
                    dmeta_count += 1
                    if not dmeta_found:
                        dmeta_found = True
                        dmeta_intersect_count += 1
        #then do nysiis
        dist = Levenshtein.distance(v_nysiss, v2_nysiss)
        longest = len(v_nysiss) if len(v_nysiss)>len(v2_nysiss) else len(v2_nysiss)
        if longest != 0:
            if dist/longest < 0.1:
                print(v_nysiss+"-"+v2_nysiss)
                nysiss_count += 1
                if not dmeta_found:
                    nysiss_found = True
                    nysiss_intersect_count += 1

#first do string
dbo_size = len(dbo_label_dict)
dbtune_size = len(dbtune_label_dict)
intersection = str_intersect_count
union = dbo_size+dbtune_size-2*intersection
jaccard = intersection/union
subset_jaccard = intersection/min(dbo_size, dbtune_size)

print("String comparison:")
print("DBO: {}, DBtune: {}, Intersection: {}, Union: {}, Jaccard: {}, Subset Jaccard: {}, Totalcount: {}".format(dbo_size, dbtune_size, intersection, union, jaccard, subset_jaccard, str_count))

#then do dmeta
dbo_size = len(dbo_label_dict)
dbtune_size = len(dbtune_label_dict)
intersection = dmeta_intersect_count
union = dbo_size+dbtune_size-2*intersection
jaccard = intersection/union
subset_jaccard = intersection/min(dbo_size, dbtune_size)

print("Dmeta comparison:")
print("DBO: {}, DBtune: {}, Intersection: {}, Union: {}, Jaccard: {}, Subset Jaccard: {}, Totalcount: {}".format(dbo_size, dbtune_size, intersection, union, jaccard, subset_jaccard, dmeta_count))

#then do nysiis
dbo_size = len(dbo_label_dict)
dbtune_size = len(dbtune_label_dict)
intersection = nysiss_intersect_count
union = dbo_size+dbtune_size-2*intersection
jaccard = intersection/union
subset_jaccard = intersection/min(dbo_size, dbtune_size)

print("NYSIIS comparison:")
print("DBO: {}, DBtune: {}, Intersection: {}, Union: {}, Jaccard: {}, Subset Jaccard: {}, Totalcount: {}".format(dbo_size, dbtune_size, intersection, union, jaccard, subset_jaccard, nysiss_count))

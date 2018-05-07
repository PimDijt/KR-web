import pickle
import Levenshtein

with open('dbo_label_dict.pickle', 'rb') as f:
    dbo_label_dict = pickle.load(f)

with open('dbtune_label_dict.pickle', 'rb') as f:
    dbtune_label_dict = pickle.load(f)

count = 0
for k, v in dbtune_label_dict.items():
    for k2, v2 in dbo_label_dict.items():
        dist = Levenshtein.distance(v, v2)
        if dist > 0:
            dist = dist-1 #Vanwege vriendelijkeheid
        longest = len(v) if len(v)>len(v2) else len(v2)
        if dist/longest < 0.2:
            print(v+"-"+v2)
            count += 1
print(len(dbo_label_dict))
print(len(dbtune_label_dict))
print(count)
print(len(dbo_label_dict)+len(dbtune_label_dict)-2*count)
print(count/(len(dbo_label_dict)+len(dbtune_label_dict)-2*count))
print("DBO: {}, DBtune: {}, Intersection: {}, Union: {}, Jaccard: {}".format(len(dbo_label_dict), len(dbtune_label_dict), count, len(dbo_label_dict)+len(dbtune_label_dict)-2*count), count/(len(dbo_label_dict)+len(dbtune_label_dict)-2*count))

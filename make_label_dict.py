import pickle

#first dbo
#24 slices of 8061
sliceSize = 8061
slices = list(range(0, (24*sliceSize), sliceSize))

dbo_label_dict = {}


for s in slices:
    print(s)
    with open('dbo_labels-'+str(s)+'.pickle', 'rb') as f:
      pick = pickle.load(f)
      for item in pick:
          subject = item["s"]
          label = item["o"]
          if "@en" in label:
              parsed_label = label.split("@en")[0].replace("\"", "")
              dbo_label_dict[subject] = parsed_label
              print("{} -> {} -> {}".format(subject, label, parsed_label))


with open('dbo_label_dict.pickle', 'wb') as handle:
    pickle.dump(dbo_label_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''
#then dbtune
#22 slices of 55555
sliceSize = 55555
slices = list(range(0, (22*sliceSize), sliceSize))

dbtune_label_dict = {}

for s in slices:
    print(s)
    with open('dbtune_labels-'+str(s)+'.pickle', 'rb') as f:
      pick = pickle.load(f)
      for item in pick:
          subject = item["s"]
          label = item["o"]
          if "@en" in label:
              parsed_label = label.split("@en")[0].replace("\"", "")
              print(parsed_label)
              dbo_label_dict[subject] = parsed_label
'''

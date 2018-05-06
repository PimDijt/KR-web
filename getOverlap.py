import pickle
import Levenshtein

with open('dbo_dict.pickle', 'rb') as f:
  dbo_dict = pickle.load(f)

with open('dbtune_dict.pickle', 'rb') as f:
  dbtune_dict = pickle.load(f)

#for s in ['1017856', '1272320', '1526784', '381696', '636160', '890624', '1081472', '1335936', '1590400', '445312', '699776', '954240', '1145088', '1399552', '254464', '508928', '763392', '1208704', '1463168', '318080', '572544', '827008']:
for s in ['1017856']:
  with open('dbo_labels-'+s+'.pickle', 'rb') as f:
    pick = pickle.load(f)
    for item in pick:
      print(item)
      print(item[0])
      print(item[1])
      print(item[2])

purlMusicArtist = set()
purlMusicArtistSl = set()
dboMusicalArtist = set()
dboMusicalArtistSl = set()

for item in dbtune_dict:
  purlMusicArtist.add(item['s'])
  purlMusicArtistSl.add(item['s'].split("/")[-1][:-1])
  if item['s'].split("/")[-1]=="":
    print(item['s'])

for item in dbo_dict:
  dboMusicalArtist.add(item['s'])
  dboMusicalArtistSl.add(item['s'].split("/")[-1][:-1])
  if item['s'].split("/")[-1]=="":
    print(item['s'])

dbo_list = list(purlMusicArtist)
dboSl_list = list(purlMusicArtistSl)
dbtune_list = list(dboMusicalArtist)
dbtuneSl_list = list(dboMusicalArtistSl)

#for idbSl in dbtuneSl_list:
#  for idboSl in dboSl_list:
#    dist = Levenshtein.distance(idbSl, idboSl)
#    if dist > 0:
#      dist = dist-1 #Vanwege vriendelijkeheid
#    longest = len(idbSl) if len(idbSl)>len(idboSl) else len(idboSl)
#    if dist/longest < 0.2:
#      print(idbSl+"-"+idboSl)

print("DBO: %d, DBtune: %d, Intersection: %d, Union: %d"%(len(dbo_list), len(dbtune_list), len(list(dboMusicalArtist.intersection(purlMusicArtist))), len(list(dboMusicalArtist.union(purlMusicArtist)))))
print("DBO: %d, DBtune: %d, Intersection: %d, Union: %d"%(len(dboSl_list), len(dbtuneSl_list), len(list(dboMusicalArtistSl.intersection(purlMusicArtistSl))), len(list(dboMusicalArtistSl.union(purlMusicArtistSl)))))

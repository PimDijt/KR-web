import pickle
import Levenshtein

with open('dbo_dict.pickle', 'rb') as f:
  dbo_dict = pickle.load(f)

with open('dbtune_dict.pickle', 'rb') as f:
  dbtune_dict = pickle.load(f)

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

for idbSl in dbtuneSl_list:
  for idboSl in dboSl_list:
    dist = Levenshtein.distance(idbSl, idboSl)
    if dist > 0:
      dist = dist-1 #Vanwege vriendelijkeheid
    longest = len(idbSl) if len(idbSl)>len(idboSl) else len(idboSl)
    if dist/longest < 0.2:
      print(idbSl+"-"+idboSl)

print("DBO: %d, DBtune: %d, Intersection: %d, Union: %d"%(len(dbo_list), len(dbtune_list), len(list(dboMusicalArtist.intersection(purlMusicArtist))), len(list(dboMusicalArtist.union(purlMusicArtist)))))
print("DBO: %d, DBtune: %d, Intersection: %d, Union: %d"%(len(dboSl_list), len(dbtuneSl_list), len(list(dboMusicalArtistSl.intersection(purlMusicArtistSl))), len(list(dboMusicalArtistSl.union(purlMusicArtistSl)))))

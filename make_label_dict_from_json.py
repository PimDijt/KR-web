import json
import pickle

result = {}

bbc_file = open('bbc.json')
bbc_string = bbc_file.read()
bbc = json.loads(bbc_string)

for line in bbc["results"]["bindings"]:
    subject = "<"+line["s"]["value"]+">"
    label = line["o"]["value"]
    result[subject] = label

magnatude_file = open('magnatude.json')
magnatude_string = magnatude_file.read()
magnatude = json.loads(magnatude_string)

for line in magnatude["results"]["bindings"]:
    subject = "<"+line["s"]["value"]+">"
    label = line["o"]["value"]
    result[subject] = label

musicbrainz_file = open('musicbrainz.json')
musicbrainz_string = musicbrainz_file.read()
musicbrainz = json.loads(musicbrainz_string)

for line in musicbrainz["results"]["bindings"]:
    subject = "<"+line["s"]["value"]+">"
    label = line["o"]["value"]
    result[subject] = label

with open('dbtune_label_dict.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

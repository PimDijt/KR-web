import requests
import pickle
import sys

result = []

def get_next_link(r):
    links = r.headers['link'].split(',')
    for link in links:
        link = link.split(';')
        if "rel=\"next\"" in  link[1]:
            return link[0]
    return None

def handle_body(r):
    body = r.content.strip().splitlines()
    for line in body:
        pieces = line.split()
        triple = {}
        triple["s"] = bytes.decode(pieces[0])
        triple["p"] = bytes.decode(pieces[1])
        triple["o"] = bytes.decode(pieces[2])
        result.append(triple)

r = requests.get('https://hdt.lod.labs.vu.nl/triple?page_size=10000&p=a&o=%3Chttp%3A//purl.org/ontology/mo/MusicArtist%3E')
handle_body(r)
link = get_next_link(r)

while link is not None:
    link = link[2:]
    link = link[:-1]
    print(link)
    r = requests.get(link)
    handle_body(r)
    link = get_next_link(r)

with open('dbtune_dict.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

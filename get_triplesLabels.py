import requests
import pickle
import sys
import time

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
        try:
            pieces = line.split()
            if len(pieces)>2:
                triple = {}
                triple["s"] = bytes.decode(pieces[0])
                triple["p"] = bytes.decode(pieces[1])
                triple["o"] = bytes.decode(pieces[2])
                result.append(triple)
        except UnicodeDecodeError:
            continue

r = requests.get('https://hdt.lod.labs.vu.nl/triple?page_size=10000&p=rdfs:label', timeout=(30, 30))
handle_body(r)
link = get_next_link(r)

while link is not None:
    link = link[2:]
    link = link[:-1]
    print(link)
    r = requests.get(link)
    while r.status_code == '502':
        time.sleep(5)
        r = requests.get(link)
    handle_body(r)
    link = get_next_link(r)

with open('labels_dict.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

'''r = requests.get('https://hdt.lod.labs.vu.nl/triple?page_size=10000&p=a&o=%3Chttp%3A//dbpedia.org/ontology/MusicalArtist%3E', timeout=(30, 30))
handle_body(r)
link = get_next_link(r)

while link is not None:
    link = link[2:]
    link = link[:-1]
    print(link)
    r = requests.get(link)
    handle_body(r)
    link = get_next_link(r)

with open('dbo_dict.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)'''

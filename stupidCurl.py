import requests
import pickle

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
    triple = {}
    for line in body:
        line = line.split()
        triple["s"] = line[0]
        triple["p"] = line[1]
        triple["o"] = line[2]
        result.append(triple)

r = requests.get('')
handle_body(r)
link = get_next_link(r)

while link is not None:
    link = link[2:]
    link = link[:-1]
    print(link)
    r = requests.get(link)
    handle_body(r)
    link = get_next_link(r)

with open('', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

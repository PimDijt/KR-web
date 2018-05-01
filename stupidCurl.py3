import requests
r = requests.get('https://hdt.lod.labs.vu.nl/triple?page_size=1&p=%3Chttp%3A//www.w3.org/1999/02/22-rdf-syntax-ns%23type%3E&o=%3Chttp%3A//purl.org/ontology/mo/MusicArtist%4E&g=%3Chttps%3A//hdt.lod.labs.vu.nl/graph/LOD-a-lot%3E')
r.headers['link'].split(',')[2]

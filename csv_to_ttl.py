import csv
from urllib.parse import quote
from csv import DictReader
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri

#in the iribaker file:
#import urllib.parse as urlparse (suddenly there is urlparse)
#    if not isinstance(iri, str): (unicode error)

filenames = ["data/lhbt-hulpverlening.csv", "data/dak-en-thuislozenzorg.csv", "data/verpleeg-en-verzorgingshuizen.csv"]
short = ["lhbt", "dakth", "verz"]
for i in range(len(filenames)):
    filename = filenames[i];
    with open(filename,'r', encoding="ISO-8859-1") as csvfile:
        # Set the right quote character and delimiter
        csv_contents = [{k: v for k, v in row.items()}
            for row in csv.DictReader(csvfile, skipinitialspace=True, quotechar='"', delimiter=';')]

    # A namespace for our resources
    data = 'http://few.vu.nl/~mvr320/KRweb/resource'
    DATA = Namespace(data)

    # A namespace for our vocabulary items (schema information, RDFS, OWL classes and properties etc.)
    vocab = 'http://few.vu.nl/~mvr320/KRweb/vocab/'
    VOCAB = Namespace(vocab)

    # The URI for our dataset
    url = 'http://few.vu.nl/~mvr320/KRweb/resource/'+short[i]
    SETNAME = Namespace(url)
    graph_uri = URIRef(url)

    # We initialize a dataset, and bind our namespaces
    dataset = Dataset()
    dataset.bind('g13data',DATA)
    dataset.bind('g13vocab',VOCAB)
    dataset.bind('gl13set',SETNAME)

    # We then get a new dataset object with our URI from the dataset.
    graph = dataset.graph(graph_uri)

    # Load the externally defined schema into the default dataset (context) of the dataset
    dataset.default_context.parse('vocab.ttl', format='turtle')

    # Let's iterate over the dictionary, and create some triples
    # Let's pretend we know exactly what the 'schema' of our CSV file is
    for row in csv_contents:

        thing = URIRef(to_iri(url+row['titel']))

        points = row['locatie'][5:].split()
        lat = points[1][:-1]
        lng = points[0][1:]

        name = Literal(row['titel'], datatype=XSD['string'])
        lat = Literal(lat, datatype=XSD['string'])#moet float worden
        lng = Literal(lng, datatype=XSD['string'])
        website = Literal(row['internet'], datatype=XSD['string'])

        #if "huisarts" in row.title:
            #add relation to class huisarts


        # All set... we are now going to add the triples to our dataset
        dataset.add((thing, VOCAB['name'], name))
        dataset.add((thing, VOCAB['lat'], lat))
        dataset.add((thing, VOCAB['lng'], lng))
        dataset.add((thing, VOCAB['website'], website))
        dataset.add((thing, RDF['type'], VOCAB['Instantie']))

    with open('outputTTL/'+short[i]+'-rdf.trig','wb') as f:
        dataset.serialize(f, format='trig')

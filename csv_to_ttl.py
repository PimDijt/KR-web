import csv
from urllib.parse import quote
from csv import DictReader
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri

#in the iribaker file:
#import urllib.parse as urlparse (suddenly there is urlparse)
#    if not isinstance(iri, str): (unicode error)

dbp = 'http://dbpedia.org/property/'
DBP = Namespace(dbp)

filenames = ["lhbt-hulpverlening.csv", "dak-en-thuislozenzorg.csv", "verpleeg-en-verzorgingshuizen.csv","zorg-voor-mensen-met-een-beperking.csv"]
short = ["lhbt", "dakth", "verz","zorbep"]
for i in range(len(filenames)):
    filename = 'data/'+filenames[i];
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
    dataset.bind('g13set',SETNAME)

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
        lat = Literal(lat, datatype=XSD['double'])
        lng = Literal(lng, datatype=XSD['double'])
        website = Literal(row['internet'], datatype=XSD['string'])

        #if "huisarts" in row.title:
            #add relation to class huisarts


        # All set... we are now going to add the triples to our dataset
        dataset.add((thing, RDFS['label'], name))
        dataset.add((thing, DBP['latitude'], lat))
        dataset.add((thing, DBP['longitude'], lng))
        dataset.add((thing, VOCAB['website'], website))
        dataset.add((thing, RDF['type'], VOCAB['Instantie']))
        if short[i] == "zorbep":
            for substr in ["Woonlocatie", "Woonvoorziening", "Kleinschalig wonen"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['night']))
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
            for substr in ["Stichting", "agcentrum", "ctiviteitencentrum"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['specialNeedCare']))
        if short[i] == "dakth":
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
            

    with open('outputTTL/'+short[i]+'-rdf.trig','wb') as f:
        dataset.serialize(f, format='trig')

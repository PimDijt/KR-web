import csv
from urllib.parse import quote
from csv import DictReader
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri

dbp = 'http://dbpedia.org/property/'
DBP = Namespace(dbp)

# A namespace for our vocabulary items (schema information, RDFS, OWL classes and properties etc.)
vocab = 'http://few.vu.nl/~mvr320/KRweb/vocab/'
VOCAB = Namespace(vocab)

# A namespace for our resources
data = 'http://few.vu.nl/~mvr320/KRweb/resource'
DATA = Namespace(data)

filenames = ["sporthallen-en-zwembaden-1.csv", "dak-en-thuislozenzorg.csv", "tandartsen.csv", "verpleeg-en-verzorgingshuizen.csv","zorg-voor-mensen-met-een-beperking.csv"]
short = ["spzw", "dakth", "tooth", "lhbt", "verz","zorbep"]
for i in range(len(filenames)):
    print(short[i])
    filename = 'data/'+filenames[i];
    with open(filename,'r', encoding="ISO-8859-1") as csvfile:
        # Set the right quote character and delimiter
        csv_contents = [{k: v for k, v in row.items()}
            for row in csv.DictReader(csvfile, skipinitialspace=True, quotechar='"', delimiter=';')]


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
        thing = ""
        
        points = ""
        lat = ""
        lng = ""
        
        name = ""
        lat = ""
        lng = ""
        website = ""
        
        # All set... we are now going to add the triples to our dataset
        if short[i] != "prk":
            thing = URIRef(to_iri(url+row['titel']))
            points = row['locatie'][5:].split()
            lat = points[1][:-1]
            lng = points[0][1:]
            name = Literal(row['titel'], datatype=XSD['string'])
            lat = Literal(lat, datatype=XSD['double'])
            lng = Literal(lng, datatype=XSD['double'])
            if short[i] != "spzw":
                website = Literal(row['internet'], datatype=XSD['string'])
            else:
                website = Literal(row['Website'], datatype=XSD['string'])
            dataset.add((thing, RDFS['label'], name))
            dataset.add((thing, DBP['latitude'], lat))
            dataset.add((thing, DBP['longitude'], lng))
            dataset.add((thing, VOCAB['website'], website))
            dataset.add((thing, RDF['type'], VOCAB['instantie']))
        else:
            thing = URIRef(to_iri(url+row['Naam']))
            lat = row['LAT']
            lng = row['LON']
            name = Literal(row['Naam'], datatype=XSD['string'])
            lat = Literal(lat, datatype=XSD['double'])
            lng = Literal(lng, datatype=XSD['double'])
            dataset.add((thing, RDFS['label'], name))
            dataset.add((thing, DBP['latitude'], lat))
            dataset.add((thing, DBP['longitude'], lng))
            dataset.add((thing, RDF['type'], VOCAB['park']))
        if short[i] == "spzw":
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['movementIssues']))
            if row['type'] == "Zwembad":
                dataset.add((thing, RDF['type'], VOCAB['swimmingPool']))
            if row['type'] == "Sporthal":
                if "Tennis" in row['titel']:
                    dataset.add((thing, RDF['type'], VOCAB['tennisHall']))
                else:
                    dataset.add((thing, RDF['type'], VOCAB['sportCentrum']))
        if short[i] == "tooth":
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['dentalIssues']))
            if "Kindertandheelkunde" in row['titel']:
                dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['child']))
            else:
                dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['adult']))                
        if short[i] == "prk":
            dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['child']))
        else:
            dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['adult']))                
        if short[i] == "dakth":
            substrdb = ["50", "work","Juttersdok", "HVO-Querido"]
            substrbw = ["huis", "begeleid", "wonen","discus", "Woon", "HVO-Querido"]
            substrih = ["jurist", "belangen", "Meldpunt", "HVO-Querido", "Stichting"]
            substrvl = ["ettafel", "Heils"]
            for esubstrdb in substrdb:
                if esubstrdb in row['titel']:
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['dayActivity']))
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['work']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessReintegration']))
            for esubstrbw in substrbw:
                if esubstrbw in row['titel']:
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['livingAccomodation']))
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['sleepLocation']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessReintegration']))
            for esubstrih in substrih:
                if esubstrih in row['titel']:
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsPrevention']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessReintegration']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessPrevention']))
            for esubstrvl in substrvl:
                if esubstrih in row['titel']:
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['food']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessReintegration']))
        if short[i] == "zorbep":
            for substr in ["Woonlocatie", "Woonvoorziening", "Kleinschalig wonen"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['night']))
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
            for substr in ["Stichting", "agcentrum", "ctiviteitencentrum"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['specialNeedCare']))
            

    with open('outputTTL/'+short[i]+'-rdf.trig','wb') as f:
        dataset.serialize(f, format='trig')

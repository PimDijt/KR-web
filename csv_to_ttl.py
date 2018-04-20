import csv
from urllib.parse import quote
from csv import DictReader
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri
import uuid 

dbp = 'http://dbpedia.org/property/'
DBP = Namespace(dbp)

dbo = 'http://dbpedia.org/ontology/'
DBO = Namespace(dbo)

wgs = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
WGS = Namespace(wgs)

# A namespace for our vocabulary items (schema information, RDFS, OWL classes and properties etc.)
vocab = 'http://few.vu.nl/~mvr320/KRweb/vocab/'
VOCAB = Namespace(vocab)

# A namespace for our resources
data = 'http://few.vu.nl/~mvr320/KRweb/resource/'
DATA = Namespace(data)

geo = 'http://www.opengis.net/ont/geosparql#'
GEO = Namespace(geo)

geof = 'http://www.opengis.net/def/function/geosparql/'
GEOF = Namespace(geof)

schema = 'http://schema.org/'
SCHEMA = Namespace(schema)

vcard = 'http://www.w3.org/2006/vcard/ns#'
VCARD = Namespace(vcard)

void = 'http://rdfs.org/ns/void#'
VOID = Namespace(void)

filenames = ["parkplantsoen.csv", "lhbt-hulpverlening.csv", "opvoedingsondersteuning.csv", "sporthallen-en-zwembaden-1.csv", "dak-en-thuislozenzorg.csv", "tandartsen.csv", "verpleeg-en-verzorgingshuizen.csv", "zorg-voor-mensen-met-een-beperking.csv", "toegankelijkheid-gebouwen-2-8-2016-2.csv"]
short = ["prk", "lhbt", "opvo", "spzw", "dakth", "tooth", "verz", "zorbep", "toe"]
for i in range(len(filenames)):
    print(short[i])
    filename = 'data/'+filenames[i];
    with open(filename,'r', encoding="ISO-8859-1") as csvfile:
        # Set the right quote character and delimiter
        csv_contents = [{k: v for k, v in row.items()}
            for row in csv.DictReader(csvfile, skipinitialspace=True, quotechar='"', delimiter=';')]


    # The URI for our dataset
    url = 'http://few.vu.nl/~mvr320/KRweb/resource/'+short[i]+'/'
    SETNAME = Namespace(url)
    graph_uri = URIRef(url)

    # We initialize a dataset, and bind our namespaces
    dataset = Dataset()
    dataset.bind('g13data',DATA)
    dataset.bind('g13vocab',VOCAB)
    dataset.bind('g13set',SETNAME)
    dataset.bind('geo', GEO)
    dataset.bind('geof',GEOF)
    dataset.bind('dbo',DBO)
    dataset.bind('dbp',DBP)
    dataset.bind('schema',SCHEMA)
    dataset.bind('vcard',VCARD)
    dataset.bind('wgs',WGS)
    dataset.bind('void',VOID)

    # We then get a new dataset object with our URI from the dataset.
    graph = dataset.graph(graph_uri)

    # Load the externally defined schema into the default dataset (context) of the dataset
    #dataset.default_context.parse('vocab.ttl', format='turtle')

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
        rndom = uuid.uuid4().hex[:16].upper()
        if short[i] != "prk":
            thing = URIRef(to_iri(url+row['titel_key']+rndom))
            thinggeo = URIRef(to_iri(url+row['titel_key']+rndom+'geo'))
            points = row['locatie'][5:].split()
            lati = points[1][:-1]
            lngi = points[0][1:]
            websiteBool = True
            name = Literal(row['titel'], datatype=XSD['string'])
            lat = Literal(lati, datatype=XSD['double'])
            lng = Literal(lngi, datatype=XSD['double'])
            latw = Literal(lati, datatype=XSD['float'])
            lngw = Literal(lngi, datatype=XSD['float'])
            addr = Literal(row['adres'], datatype=XSD['string'])
            pcode = Literal(row['postcode'], datatype=XSD['string'])
            point = Literal(row['locatie'], datatype=GEO['wktLiteral'])
            if short[i] != "toe":
                if short[i] != "spzw":
                    if short[i] != 'dakth':
                        if row['internet'] != "":
                            website = Literal(row['internet'], datatype=XSD['string'])
                        else:
                            websiteBool = False
                    else:
                        if 'http' in row['straat']:
                            website = Literal(row['straat'], datatype=XSD['string'])
                        elif 'http' in row['internet']:
                            website = Literal(row['internet'], datatype=XSD['string'])
                        elif 'http' in row['plaats_2']:
                            website = Literal(row['plaats_2'], datatype=XSD['string'])
                        else:
                            websiteBool = False
                else:
                    website = Literal(row['Website'], datatype=XSD['string'])
            dataset.add((thing, RDFS['label'], name))
            dataset.add((thing, DBP['latitude'], lat))
            dataset.add((thing, DBP['longitude'], lng))
            dataset.add((thing, WGS['lat'], latw))
            dataset.add((thing, WGS['long'], lngw))
            dataset.add((thing, GEO['hasGeometry'], thinggeo))
            dataset.add((thinggeo, RDF['type'], GEO['Geometry']))
            dataset.add((thinggeo, GEO['asWKT'], point))
            dataset.add((thing, SCHEMA['postalCode'], pcode))
            dataset.add((thing, VCARD['hasPostalCode'], pcode))
            dataset.add((thing, DBO['PostalCode'], pcode))
            dataset.add((thing, SCHEMA['PostalAddress'], addr))
            dataset.add((thing, VCARD['hasAddress'], addr))
            dataset.add((thing, DBO['address'], addr))
            #eventueel voor BAG
            if short[i]!="toe":
                if websiteBool:
                    dataset.add((thing, VOCAB['website'], website))
                    dataset.add((thing, DBO['Website'], website))
                    dataset.add((thing, SCHEMA['WebSite'], website))
                    dataset.add((thing, RDFS['seeAlso'], website))
            dataset.add((thing, RDF['type'], VOCAB['instantie']))
        else:
            thing = URIRef(to_iri(url+row['Naam']+rndom))
            thinggeo = URIRef(to_iri(url+row['Naam']+rndom+'geo'))
            lati = row['LAT'].replace(',','.')
            lngi = row['LNG'].replace(',','.')
            point = Literal('POINT( '+row['LNG']+' '+row['LAT']+' )', datatype=GEO['wktLiteral'])
            name = Literal(row['Naam'], datatype=XSD['string'])
            lat = Literal(lati, datatype=XSD['double'])
            lng = Literal(lngi, datatype=XSD['double'])
            latw = Literal(lati, datatype=XSD['float'])
            lngw = Literal(lngi, datatype=XSD['float'])
            dataset.add((thing, RDFS['label'], name))
            dataset.add((thing, DBP['latitude'], lat))
            dataset.add((thing, DBP['longitude'], lng))
            dataset.add((thing, WGS['lat'], latw))
            dataset.add((thing, WGS['long'], lngw))
            dataset.add((thing, GEO['hasGeometry'], thinggeo))
            dataset.add((thinggeo, RDF['type'], GEO['Geometry']))
            dataset.add((thinggeo, GEO['asWKT'], point))
            dataset.add((thing, RDF['type'], VOCAB['park']))
        if short[i] == "spzw":
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['movementIssues']))
            if row['type'] == "Zwembad":
                dataset.add((thing, RDF['type'], VOCAB['swimmingPool']))
            if row['type'] == "Sporthal":
                if "Tennis" in row['titel']:
                    dataset.add((thing, RDF['type'], VOCAB['tennisHall']))
                else:
                    dataset.add((thing, RDF['type'], VOCAB['sportcentrum']))
        if short[i] == "tooth":
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['dentalIssues']))
            if "Kindertandheelkunde" in row['titel']:
                dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['children']))
            else:
                dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['children']))
                dataset.add((thing, VOCAB['providesDentalcareTo'], VOCAB['adults']))                
        if short[i] == "dakth":
            substrdb = ["50", "Inloophuis", "work","Juttersdok", "HVO-Querido"]
            substrbw = ["doorstroomhuis", "begeleid", "wonen","discus", "Woon", "HVO-Querido"]
            substrih = ["jurist", "Bosco", "elangen", "Meldpunt", "HVO-Querido", "Stichting"]
            substrvl = ["ettafel", "Heils", "Inloophuis"]
            for esubstrdb in substrdb:
                if esubstrdb in row['titel']:
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['dayActivity']))
                    if "Inloophuis" not in row['titel']:
                        dataset.add((thing, VOCAB['providesReintegration'], VOCAB['work']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['addictsReintegration']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['homelessReintegration']))
            for esubstrbw in substrbw:
                if esubstrbw in row['titel']:
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['livingAccomodation']))
                    dataset.add((thing, VOCAB['providesReintegration'], VOCAB['placeToSleep']))
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
                    dataset.add((thing, VOCAB['providesSpecialCareTo'], VOCAB['disabledPeople']))
                    #dataset.add((thing, RDF['type'], VOCAB['dayLocation']))
                    #dataset.add((thing, RDF['type'], VOCAB['nightLocation']))
            for substr in ["Stichting", "agcentrum", "ctiviteitencentrum"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
                    if "Stichting" not in row['titel']:
                        dataset.add((thing, VOCAB['providesSpecialCareTo'], VOCAB['disabledPeople']))
                    #dataset.add((thing, RDF['type'], VOCAB['dayLocation']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['disabledPeopleCare']))
        if short[i] == "verz":
            for substr in ["erpleeghuis", "oon", "org"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesSpecialCareTo'], VOCAB['elderly']))
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['night']))
                    dataset.add((thing, VOCAB['providesSpecialCare'], VOCAB['day']))
                    #dataset.add((thing, RDF['type'], VOCAB['dayLocation']))
                    #dataset.add((thing, RDF['type'], VOCAB['nightLocation']))
            for substr in ["reuma"]:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['reumaCare']))
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['movementIssues']))
            if "Joods" in row['titel']:
                dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['jewElderlyCare']))
            else:
                dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['elderlyCare']))
        if short[i] == "toe":
            newClass = URIRef(to_iri('http://few.vu.nl/~mvr320/KRweb/vocab/'+row['type'].replace("/", "ting")))
            dataset.add((thing, RDF['type'], newClass))
            dataset.add((newClass, RDFS['subClassOf'], VOCAB['disabledLocations']))
            #dataset.add((newClass, RDFS['label'], Literal(row['type'], lang="nl")))#, datatype=XSD['string'])))
            if row['type'] != "Huisartsenposten":
                dataset.add((newClass, RDFS['label'], Literal(row['type_en'], lang="en")))#, datatype=XSD['string'])))
            else:
                dataset.add((newClass, RDFS['label'], Literal(row['type_en']+" - Out of office hours", lang="en")))#, datatype=XSD['string'])))
        if short[i] == "opvo":
            substrkg = ["ezond", "pvoed", "OKT"]
            for substr in substrkg:
                if substr in row['titel']:
                    dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['childDevelopment']))
            substrkg = ["peel", "pel"]
            if substr in row['titel']:
                dataset.add((thing, VOCAB['providesExercisesFor'], VOCAB['children']))
            #dataset.add((thing, RDF['type'], VOCAB['childDevelopmentCenter']))
        if short[i] == "lhbt":
            substr = ["COC", "Hiv","Coaching", "Trans", "seksuele identiteit"]
            for subs in substr:
                if subs in row['titel']:
                    dataset.add((thing, VOCAB['providesCoachingAbout'], VOCAB['lhbtIssues']))
            dataset.add((thing, VOCAB['providesInformationAbout'], VOCAB['lhbtIssues']))
            #Vieze dataset...
    with open('outputTTL/'+short[i]+'-rdf.ttl','wb') as f:
        dataset.serialize(f, format='turtle')

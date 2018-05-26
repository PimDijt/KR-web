import pickle
import sys
import requests
import urllib.parse
import time

with open('dbo_dict.pickle', 'rb') as f:
    dbo_dict = pickle.load(f)

with open('dbtune_dict.pickle', 'rb') as f:
    dbtune_dict = pickle.load(f)

result = []

renewTerm= []

def get_label(term, session):
    url = "https://hdt.lod.labs.vu.nl/triple?p=rdfs:label&s="+urllib.parse.quote_plus(term)
    #print(url)
    try:
        r = session.get(url)
    except ConnectionError:
        time.sleep(5)
        get_label(term, session)
    while r.status_code=="502":
        time.sleep(1)
        #print("Gateway")
        r = session.get(url)
    #print("Got request")
    body = r.content.strip().splitlines()
    #print("Got Stripped")
    if body != []:
        print("Got a none empty body")
        for line in body:
            line = line.split()
            triple = {}
            #print(line)
            try:
                triple["s"] = bytes.decode(line[0])
                triple["p"] = bytes.decode(line[1])
                triple["o"] = ""
                for i in range(len(line)):
                    if i>=2:
                        triple["o"] += bytes.decode(line[i])
                result.append(triple)
            except IndexError:
                renewTerm.append(term)


'''count = 0
counterNumber = int(sys.argv[1])
sliceSize = 2686#63616

with requests.Session() as session:
    for item in dbo_dict:
        if count >= counterNumber*sliceSize:
            if count < (counterNumber+1)*sliceSize:
                term = item["s"]
                print("{} / {}".format(count, len(dbo_dict)))
                get_label(term, session)
                with open('dbo_labels-'+str(counterNumber*sliceSize)+'.pickle', 'wb') as handle:
                    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("{} / {} - done".format(count, len(dbo_dict)))
        count += 1
    print("Renew list")
    for term in renewTerm:
        time.sleep(1)
        get_label(term, session)
        with open('dbo_labels-'+str(counterNumber*sliceSize)+'.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''
count = 0
counterNumber = int(sys.argv[1])
sliceSize = 18518

renewTerm = []

with requests.Session() as session:
    for item in dbtune_dict:
        if count >= counterNumber*sliceSize:
            if count < (1+counterNumber)*sliceSize:
                term = item["s"]
                print("{} / {}".format(count, len(dbo_dict)))
                get_label(term, session)
                #print("{} / {} - done".format(count, len(dbo_dict)))
        count += 1
    print("Renew list")
    for item in renewTerm:
        get_label(term, session)

with open('dbtune_labels-'+str(counterNumber*sliceSize)+'.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

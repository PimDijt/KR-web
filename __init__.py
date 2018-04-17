from flask import Flask, render_template, url_for, request, jsonify, redirect
from SPARQLWrapper import SPARQLWrapper, RDF, JSON
import requests
import csv
import traceback
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/map')
def map():
    detlz = parse_csv('dak-en-thuislozenzorg.csv')
    lhbt = parse_csv('lhbt-hulpverlening.csv')
    zorg = parse_csv('verpleeg-en-verzorgingshuizen.csv')
    result = [(0, "green", True, detlz), (1, "red", True, lhbt), (2, "blue", True, zorg)]
    return render_template('google_maps.html', results = result)

@app.route('/map_filter')
def map_filter():
    detlz = parse_csv('dak-en-thuislozenzorg.csv')
    lhbt = parse_csv('lhbt-hulpverlening.csv')
    zorg = parse_csv('verpleeg-en-verzorgingshuizen.csv')
    result = [(0, "dak-en-thuislozenzorg", "green", "true", detlz), (1, "lhbt-hulpverlening", "red", "true", lhbt), (2, "verpleeg-en-verzorgingshuizen", "blue", "true", zorg)]
    return render_template('google_maps_filter.html', results = result)

@app.route('/map_test')
def map_test():
    '''filter_query = "prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    filter_query += "prefix owl: <http://www.w3.org/2002/07/owl#> "
    filter_query += "prefix xsd: <http://www.w3.org/2001/XMLSchema#> "
    filter_query += "prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    filter_query += "select ?s ?p ?o WHERE{ ?s rdfs:subClassOf ?o }"'''
    filter_query = "prefix rdf%3A <http%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23>%0Aprefix owl%3A <http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23>%0Aprefix xsd%3A <http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23>%0Aprefix rdfs%3A <http%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23>%0A%0ASELECT %3Fsup %3Fsub WHERE {%0A%20 %3Fsupt rdfs%3AsubClassOf%2B g13vocab%3ALocation .%0A%20 %3Fsupt rdfs%3AsubClassOf%3F g13vocab%3ALocation .%0A%20 %3Fsubt rdfs%3AsubClassOf %3Fsupt .%0A%20 %3Fsubt rdfs%3Alabel %3Fsub .%0A%20 %3Fsupt rdfs%3Alabel %3Fsup .%0A}"
    url = "/sparql?endpoint=http://localhost:5820/KRweb/query/&query="+filter_query
    return redirect(url)
    #return render_template('google_maps_overlap_test.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/sparql', methods=['GET'])
def sparql():
    endpoint = request.args.get('endpoint', None)
    query = request.args.get('query', None)
    return_format = request.args.get('format','JSON')

    if endpoint and query :
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)

        if return_format == 'RDF':
            sparql.setReturnFormat(RDF)
        else :
            sparql.setReturnFormat(JSON)
            sparql.addParameter('Accept','application/sparql-results+json')

        #sparql.addParameter('reasoning','true')
        try :
            response = sparql.query().convert()
            if return_format == 'RDF':
                return response.serialize(format='turtle')
            else:
                return make_filter_page(response["results"]["bindings"])
                #return jsonify(response)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'result': 'Error'})
    else :
        return jsonify({'result': 'Error'})

@app.route('/sparql2', methods=['GET'])
def sparql2():
    endpoint = request.args.get('endpoint', None)
    query = request.args.get('query', None)
    return_format = request.args.get('format','JSON')

    if endpoint and query :
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)

        if return_format == 'RDF':
            sparql.setReturnFormat(RDF)
        else :
            sparql.setReturnFormat(JSON)
            sparql.addParameter('Accept','application/sparql-results+json')

        #sparql.addParameter('reasoning','true')
        try :
            response = sparql.query().convert()
            if return_format == 'RDF':
                return response.serialize(format='turtle')
            else:
                #return make_filter_page(response["results"]["bindings"])
                return jsonify(response)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'result': 'Error'})
    else :
        return jsonify({'result': 'Error'})

def make_filter_page(filter_data):
    result = {}
    for item in filter_data:
        if not item["sup"]["value"] in result:
            result[item["sup"]["value"]] = [item["sub"]["value"]]
        else:
            result[item["sup"]["value"]].append(item["sub"]["value"])
    return render_template('google_maps_final.html', results=result)

def parse_csv(filename):
    with open('data/'+filename, 'r', encoding="ISO-8859-1") as f:
         tmp = csv.reader(f, delimiter=';')
         headings = next(tmp)

         title_index = headings.index("titel")
         location_index = headings.index("locatie")

         result = []
         count = 0
         for row in tmp:
             title = row[title_index]
             points = row[location_index][5:].split()
             lat = points[1][:-1]
             lng = points[0][1:]
             result.append((count, title, lat, lng))
             count += 1
    return result

if __name__ == '__main__':
      app.run(debug=True)

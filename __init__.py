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

@app.route('/map_final')
def map_test():
    return render_template('google_maps_final.html')

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

if __name__ == '__main__':
      app.run(debug=True)

from flask import Flask, render_template, url_for, request, jsonify, redirect
from SPARQLWrapper import SPARQLWrapper, RDF, JSON
import requests
import csv
import traceback
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map')
def map():
    return render_template('google_maps.html')

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

        sparql.addParameter('reasoning','true')
        try :
            response = sparql.query().convert()
            if return_format == 'RDF':
                return response.serialize(format='turtle')
            else:
                return jsonify(response)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'result': 'Error'})
    else :
        return jsonify({'result': 'Error'})

if __name__ == '__main__':
      app.run(debug=True)

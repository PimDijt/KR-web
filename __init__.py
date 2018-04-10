from flask import Flask
from flask import render_template
import csv

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
    return render_template('google_maps_overlap_test.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

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

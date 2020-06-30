import os
from flask import Flask, request, url_for, redirect,render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_form', methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        return redirect(url_for('index'))
        # species = request.form.get('species')
        # return f'''<h1>The species is: {species}</h1> '''
    return render_template('search_form.html')

@app.route('/search_results')
def search_results():
    species = request.args.get('species')
    return f'''<h1>The species is: {species}</h1> '''

    # params = {
    #     'q': species,
    # }
    # response = requests.get('https://www.fishwatch.gov/api/species')
    # json_response = response.json()
    # species_name = json_response[1]
    # return species_name

@app.route('/all_species')
def get_all():
    r = requests.get('https://www.fishwatch.gov/api/species')

    # species = json.loads(r.text)
    json_response = r.json()
    length = len(json_response)
    # name = json_response['Species Name']
    # response = json.dumps(json_response)
    for i in json_response:
        return i
    # response = json_response[1]
    # print(json_response)
    # return response
    # return render_template('all.html', response=response)
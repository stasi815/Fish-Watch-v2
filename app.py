import os
from flask import Flask, request, url_for, redirect,render_template
import requests
import re
import json
import sys

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
    #     'Species Name': species,
    # }
    # response = requests.get('https://www.fishwatch.gov/api/species/get', params=params)
    # json_response = response.json()
    # species_name = json_response[1]
    # return response

@app.route('/all_species')
def get_all():
    r = requests.get('https://www.fishwatch.gov/api/species')

    response = str(r.text)

    # response_words = response.split()

    # word_list = []
    # for word in response_words:
    #     word_list.append(word)

    # new_string = " ".join(word_list)

    edited_response = response.replace('\\n', ' ').replace('\\u', " ").replace('\\', "").replace('\&nbsp;', "")

    stripped = re.sub('<[^<]+?>|\[{|\}]|\}|\{', '', edited_response)


    return render_template('all.html', stripped=stripped)

    # species = json.loads(r.text)
    # json_response = r.json()
    # length = len(json_response)
    # name = json_response['Species Name']
    # response = json.dumps(json_response)

    # response = json_response[1]
    # print(json_response)
    # return response
    # return render_template('all.html', response=response)
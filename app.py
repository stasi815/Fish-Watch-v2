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

    r = requests.get('https://www.fishwatch.gov/api/species')

    response = r.json()

    if request.method == 'POST':
        return redirect(url_for('index'))
        # species = request.form.get('species')
        # return f'''<h1>The species is: {species}</h1> '''
    return render_template('search_form.html', response=response)

@app.route('/search_results')
def search_results():

    species = request.args.get('species')
    
    print(species)

    r = requests.get('https://www.fishwatch.gov/api/species')

    response = r.json()



    return render_template('search_results.html', response=response, species=species)

    # return f'''<h1>The species is: {species}</h1> '''

    # params = {
    #     'Species Name': species,
    # }
    # response = requests.get('https://www.fishwatch.gov/api/species/get', params=params)
    # json_response = response.json()
    # species_name = json_response[1]
    # return response

def strip_html(content):

    new_content = content.text

    edited_text = new_content.replace('\\n', ' ').replace('\\u', " ").replace('\\', "").replace('&nbsp;', " ").replace('","', '\n').replace('"', '').replace('src:', "")

    stripped_content = re.sub('<[^<]+?>|\[{|\}]|\}|\{', '', edited_text)

    return stripped_content

@app.route('/all_species')
def get_all():

    r = requests.get('https://www.fishwatch.gov/api/species')

    # response = strip_html(r)
    response = r.json()


    return render_template('all.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
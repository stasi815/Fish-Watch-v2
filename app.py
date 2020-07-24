import os
from flask import Flask, request, url_for, redirect,render_template
import requests
import re
import json
import sys


app = Flask(__name__)

@app.route('/')
def index():
    """ Renders template for landing page """

    return render_template('index.html')

@app.route('/search_form', methods=['GET', 'POST'])
def search_form():
    """ Renders the search form and a list of all the species in Fish Watch """
    if request.method == 'POST':
        return redirect(url_for('search_results'))

    url = 'https://www.fishwatch.gov/api/species'
    r = requests.get(url)
    response = r.json()


    return render_template('search_form.html', response=response)

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    """ Renders a single species with corresponding data """

    if request.form['species']:
        result = request.form['species']
        print(result)
    else:
        result = ''

    url = f'https://www.fishwatch.gov/api/species/{result}'

    r = requests.get(url)
    response = r.json()
    
    if len(response) > 0:
        search_results = response[0]
    else:
        search_results = None

    if search_results != None:
        if search_results['Habitat'] != None:
            hab = search_results['Habitat']
            habitat = strip_html(hab)
        else:
            habitat = 'No habitat information available'

        image = search_results['Image Gallery']
        print(image)
        if image != None:
            if isinstance(image, list):
                pic = image[0]
                img_url = pic['src']
                print(img_url)
            elif isinstance(image, dict):
                img_url = image['src']
                print(img_url)
        else:
            img_url = None

    print(url)


    return render_template('search_results.html', response=response, habitat=habitat, img_url=img_url)

def strip_html(content):
    """ Strips html characters from JSON data """
    # new_content = content.text

    edited_text = content.replace('\\n', ' ').replace('\\u', " ").replace('\\', "").replace('&nbsp;', " ").replace('","', '\n').replace('"', '').replace('src:', "")

    stripped_content = re.sub('<[^<]+?>|\[{|\}]|\}|\{', '', edited_text)

    return stripped_content

@app.route('/all_species')
def get_all():
    """ Renders a list of all species and a blurb about their sustainability """


    url = 'https://www.fishwatch.gov/api/species'

    r = requests.get(url)

    response = r.json()


    return render_template('all.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
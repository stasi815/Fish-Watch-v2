import os
from flask import Flask, request, url_for, redirect,render_template
import requests
import re
import json
import sys

app = Flask(__name__)

def strip_html(content):
    """ Strips html characters from JSON data """
    # new_content = content.text

    edited_text = content.replace('\\n', ' ').replace('\\u', " ").replace('\\', "").replace('&nbsp;', " ").replace('","', '\n').replace('"', '').replace('src:', "")

    stripped_content = re.sub('<[^<]+?>|\[{|\}]|\}|\{', '', edited_text)

    return stripped_content

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

        image = search_results['Species Illustration Photo']
        print(image)
        if image != None:
            if isinstance(image, list):
                pic = image[0]
                img_url = pic['src']
                error_message = None
            elif isinstance(image, dict):
                img_url = image['src']
                error_message = None
        else:
            img_url = None

        if search_results['Population'] != None:
            population = search_results['Population']
            population = strip_html(population)
        else:
            population = 'No population information available'

        if search_results['Habitat Impacts'] != None:
            hab_impacts = search_results['Habitat Impacts']
            impacts = strip_html(hab_impacts)
            error_message = None
        else:
            impacts = 'No habitat impact information available'

        if search_results['Location'] != None:
            place = search_results['Location']
            location = strip_html(place)
            error_message = None
        else:
            impacts = 'No location information available'

        if search_results['Fishing Rate'] != None:
            rate = search_results['Fishing Rate']
            rate = strip_html(rate)
            error_message = None
        else:
            impacts = 'No fishing rate information available'

        if search_results['Bycatch'] != None:
            bycatch = search_results['Bycatch']
            bycatch = strip_html(bycatch)
            error_message = None
        else:
            impacts = 'No bycatch information available'

        if search_results['Availability'] != None:
            availability = search_results['Availability']
            availability = strip_html(availability)
            error_message = None
        else:
            impacts = 'No availability information available'

        if search_results['Harvest'] != None:
            harvest = search_results['Harvest']
            harvest = strip_html(harvest)
            error_message = None
        else:
            impacts = 'No harvest information available'

        if search_results['Harvest Type'] != None:
            harvest_type = search_results['Harvest Type']
            harvest_type = strip_html(harvest_type)
            error_message = None
        else:
            impacts = 'No harvest type information available'

        if search_results['Source'] != None:
            source = search_results['Source']
            source = strip_html(source)
            error_message = None
        else:
            impacts = 'No source information available'
    else:
        error_message = "Entry does not exist in database"
        habitat = None
        img_url = None

    return render_template('search_results.html', response=response, habitat=habitat, img_url=img_url, error_message=error_message, impacts=impacts, location=location, bycatch=bycatch, rate=rate, harvest=harvest, harvest_type=harvest_type, source=source, availability=availability, population=population)

@app.route('/all_species')
def get_all():
    """ Renders a list of all species and a blurb about their sustainability """

    url = 'https://www.fishwatch.gov/api/species'
    r = requests.get(url)
    response = r.json()

    return render_template('all.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import os
from datetime import datetime
import logging

app = Flask(__name__)

NASA_API_KEY = os.environ.get('NASA_API_KEY')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/apod')
def apod():
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    resp = requests.get(url)
    logging.debug(f'APOD API response: {resp.text}')
    if resp.ok:
        try:
            data = resp.json()
            # Ensure required fields exist
            if not all(k in data for k in ('url', 'title', 'explanation', 'date')):
                return render_template('apod.html', data=None, error='Incomplete APOD data received.')
            return render_template('apod.html', data=data)
        except Exception as e:
            return render_template('apod.html', data=None, error=f'Error parsing APOD data: {e}')
    else:
        return render_template('apod.html', data=None, error='Failed to fetch APOD')

@app.route('/neo')
def neo():
    from datetime import date
    today = date.today().isoformat()
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={NASA_API_KEY}'
    resp = requests.get(url)
    logging.debug(f'NEO API response: {resp.text}')
    neos = []
    error = None
    if resp.ok:
        try:
            data = resp.json()
            neos = data.get('near_earth_objects', {}).get(today, [])
            # Validate structure
            if not isinstance(neos, list):
                error = 'Malformed NEO data received.'
                neos = []
        except Exception as e:
            error = f'Error parsing NEO data: {e}'
    else:
        error = 'Failed to fetch NEO data.'
    return render_template('neo.html', neos=neos, date=today, error=error)

@app.route('/earth')
def earth():
    # Get date from query parameters, default to 2026-05-12
    year = request.args.get('year', '2026')
    month = request.args.get('month', '05')
    day = request.args.get('day', '12')
    date_str = f"{year}-{month.zfill(2)}-{str(day).zfill(2)}"
    meta_url = f"https://epic.gsfc.nasa.gov/api/natural/date/{date_str}"
    error = None
    images = []
    try:
        meta_resp = requests.get(meta_url)
        if meta_resp.ok:
            arr = meta_resp.json()
            for item in arr:
                name = item['image'] + '.png'
                archive = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month.zfill(2)}/{str(day).zfill(2)}/png/"
                source = archive + name
                images.append(source)
        else:
            error = f"No images found for {date_str}."
    except Exception as e:
        error = f"Error fetching images: {e}"
    return render_template('earth.html', images=images, error=error, year=year, month=month, day=day)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# NASA Demo Flask App

This Flask web application demonstrates integration with several NASA public APIs. It is designed for cloud deployment training and showcases endpoints that require an API key and render dynamic web pages.

## Features

- **Home Page** (`/`): Lists available NASA API endpoints.
- **Astronomy Picture of the Day** (`/apod`): Displays NASA's Astronomy Picture of the Day with image and explanation.
- **Near Earth Objects** (`/neo`): Lists near-Earth asteroids for today, including size and hazard info.
- **Earth Imagery** (`/earth`): Displays satellite imagery for a fixed Earth date.

## Requirements

- Python 3.8+
- Flask
- requests
- gunicorn

## NASA API Key

- Register for a free API key at [api.nasa.gov](https://api.nasa.gov/).
- Set the environment variable `NASA_API_KEY` before running the app:

## Setup

1. **Clone the repository**
2. **Install Python**
3. **Install Python dependencies using pip**
4. **Set the NASA API Key** (see above)
5. **Check the app runs manually - the app runs on port 5000**
   ```bash
   python app.py
   ```
6. **Configure nginx reverse proxy**
7. **Set up gunicorn to run the app as a WSGI server**
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
8. Use a process manager (like systemd) to keep Gunicorn running in the background and on startup.

## File Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates for each endpoint
- `requirements.txt` - (Optional) List of dependencies

## Notes

- All endpoints render as user-friendly webpages.
- The app is suitable for deployment training and can be extended for further exercises.
- NASA API rate limits apply when using the `DEMO_KEY`.

# Catalog Site
An e-Catalog displays a collection of sport gears. Data is stored in database and served via a web app interface. Item data modification is allowed for authenticated users. Social login and registration are supported. The stack used is Flask, SQLAlchemy and PostgreSQL. Documentation is carefully constructed and beautifully presented by Apiary.

## Dependencies

Use pip to install dependencies:

`pip install requirements.txt`

## Requirements

- You need to have a google plus dev account at [https://console.developers.google.com/](https://console.developers.google.com/)
- Create an app (web) and create an OAuth2 credentials client ID.
- Add the following redirect URIs:
    + `http://localhost:5001/gconnect`
    + `http://localhost:5001/login`
- Download the json which contains CLIENT_ID and CLIENT_SECRET and save it as `client_secrets.json` in the repo directory.

## Usage
- Install dependencies
- Change directory to the repo directory
- Setup database (SQLite3), if existing database file is found, you will be asked whether to delete the old one.

`python setup.py`

- Run the python script to start the server

`python views.py`

- By default, website is served at `localhost:5001`

## Documentation

API:
- Documented in `api.md`
- To view the API in pretty format, use [Apiary](http://apiary.io) to load the `api.md`.
- Otherwise, you can view it in any plain text viewer.

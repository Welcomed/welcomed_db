##Backend database/server for Welcomed

Using Flask and sqlite.

To install:

1. Clone the repo - `git clone https://github.com/Welcomed/welcomed_db.git`

2. Install Flask - `pip install Flask`

3. Create a python file called `key.py`, inside define a constant called `GOOG_KEY` that contains a Maps API key

3. `export FLASK_APP=welcomed_backend`

4. Run the server - `flask run`

If you get an import error when running the server, do `export PYTHONPATH='.'`

Data is returned in json format by GET requesting `/data/<table>`, where `<table>` is the name of the database table (at this stage either `hospitals`, `doctors`, `mentalhealth`, `realestate`).

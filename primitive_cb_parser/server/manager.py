from flask import Flask
import time

from rest_api import RestApiEngine
from settings import ParserSettings
from db_agent import DB_Agent


settings = ParserSettings()
dbagent = DB_Agent(settings)
api = RestApiEngine(settings, dbagent)
api.start_dbagent()
app = Flask(__name__)


def start(debug):
    app.run(debug=debug)


@app.route('/api/ping')
def _ping():
    return api.ping_parser_server()


@app.route('/api/progress')
def _status():
    return api.dbagent_get_progress()

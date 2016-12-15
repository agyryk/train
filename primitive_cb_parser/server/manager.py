from flask import Flask
import time

from rest_api import RestApiEngine
from db_agent import DB_Agent


dbagent = DB_Agent()
api = RestApiEngine(dbagent)
api.start_dbagent()
app = Flask(__name__)


def start(debug):
    app.run(host='0.0.0.0', debug=debug)


@app.route('/api/ping')
def _ping():
    return api.ping_parser_server()


@app.route('/api/progress')
def _status():
    return api.dbagent_get_progress()

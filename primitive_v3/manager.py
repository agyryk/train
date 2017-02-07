from flask import Flask, request
from api import RestApiEngine
import time

app = Flask(__name__)
api = RestApiEngine()


def start(debug):
    app.run(host='0.0.0.0', debug=debug)


@app.route('/api/ping')
def _ping():
    return api.ping()


@app.route('/api/run', methods=['POST'])
def _start():
    if request.json:
        api.run(request.json)
        time.sleep(1)
        return api.get_status()
    else:
        return "No request body received \n"


@app.route('/api/progress')
def _status():
    return api.get_status()


@app.route('/api/index_stats')
def _index_stats():
    return api.get_index_stats()


@app.route("/api/query", methods=['POST'])
def _query():
    if request.json:
        return api.query(request.json)
    else:
        return "No request body received \n"

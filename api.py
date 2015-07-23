import json
import os
import requests
from flask import Flask, request
from flask.ext.basicauth import BasicAuth


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("ES_BROKER_USERNAME", 'admin')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("ES_BROKER_PASSWORD", 'password')

basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.environ.get("ELASTICSEARCH_PORT", '9200')


@app.route("/resources/plans", methods=["GET"])
def plans():
    plans = [{"name": "shared_data", "description": "shared elasticsearch server"}]
    return json.dumps(plans), 200


@app.route("/resources", methods=["POST"])
def add_instance():
    # use the given parameters to create the instance
    return "", 201


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
    return "", 200


@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind_app(name):
    envs = {
        "ELASTICSEARCH_HOST": ELASTICSEARCH_HOST,
        "ELASTICSEARCH_PORT": ELASTICSEARCH_PORT,
    }
    return json.dumps(envs), 201


@app.route("/resources/<name>/bind", methods=["POST"])
def bind(name):
    return "", 201


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    elasticsearch_url = "http://{0}:{1}/".format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
    es_state = requests.get(elasticsearch_url)
    if es_state.status_code == 200:
        return "", 204
    else:
        Flask.abort(500)


@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind_app(name):
    return "", 200


@app.route("/resources/<name>/bind", methods=["DELETE"])
def unbind(name):
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))

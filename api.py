import json
import socket
import fcntl
import struct
import os
from flask import Flask, request
from flask.ext.basicauth import BasicAuth


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("ES_BROKER_USERNAME", 'admin')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("ES_BROKER_PASSWORD", 'password')

basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True

ELASTICSEARCH_IP = os.environ.get("ELASTICSEARCH_IP")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


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
    if ELASTICSEARCH_IP:
        ELASTICSEARCH_HOST = ELASTICSEARCH_IP
    else:
        ELASTICSEARCH_HOST = get_ip_address('eth0')

    envs = {
        "ELASTICSEARCH_HOST": ELASTICSEARCH_HOST,
        "ELASTICSEARCH_PORT": '9200',
    }
    return json.dumps(envs), 201


@app.route("/resources/<name>/bind", methods=["POST"])
def bind(name):
    return "", 201


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    # check the status of the instance named "name"
    return "", 204


@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind_app(name):
    return "", 200


@app.route("/resources/<name>/bind", methods=["DELETE"])
def unbind(name):
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))

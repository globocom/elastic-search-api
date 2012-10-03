import bottle
import json


app = bottle.default_app()
ELASTIC_SEARCH_URL = "10.2.122.2"


@bottle.route("/resources", method="POST")
def add():
    bottle.response.status = 201
    return ""


@bottle.route("/resources/<name>", method="POST")
def bind(name):
    bottle.response.status = 201
    return json.dumps({"ELASTIC_SEARCH_URL": ELASTIC_SEARCH_URL})


@bottle.route("/resources/<name>", method="DELETE")
def unbind(name):
    return ""


def remove():
    return ""


if __name__ == "__main__":
    bottle.run()

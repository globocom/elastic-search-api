import bottle
import json


ELASTIC_SEARCH_URL = "10.2.122.2"


def add():
    return bottle.Response(status=201)


def bind():
    b = json.dumps({"ELASTIC_SEARCH_URL": ELASTIC_SEARCH_URL})
    return bottle.Response(body=b, status=201)


def unbind():
    return bottle.Response(status=200)


def remove():
    return bottle.Response(status=200)


if __name__ == "__main__":
    bottle.run()

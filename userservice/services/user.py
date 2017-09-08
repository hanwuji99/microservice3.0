from werkzeug.exceptions import NotFound, ServiceUnavailable
import requests
from . import nice_json
from flask import Flask, request
from database.user import Users

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "add_user": "/add",
            "users": "/all",
            "user": "/all/<username>",
            "collections": "/all/<username>/collections",
        }
    })


@app.route("/add", methods=['POST'])
def add():
    form = request.form
    u = Users.new(form)
    u = u.json()
    return nice_json(u)


@app.route('/all')
def all():
    us = Users.all()
    us = [i.json() for i in us]
    return nice_json(us)


@app.route("/all/<username>")
def find_by(username):
    try:
        c = Users.find_by(username=username)
        c = c.json()
        return nice_json(c)
    except:
        raise NotFound


@app.route("/all/<username>/collections")
def user_collections(username):
    try:
        users_collections = requests.get("collectionservice/all/{}".format(username))

    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The Collections service is unavailable.")

    if users_collections.status_code == 404:
        raise NotFound("No collection were found for {}".format(username))
    users_collections = users_collections.json()
    return nice_json(users_collections)

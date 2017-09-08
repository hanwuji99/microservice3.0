from . import nice_json
from flask import Flask, request
from werkzeug.exceptions import NotFound, ServiceUnavailable
from database.collections import Collections
import requests

app = Flask(__name__)


@app.route("/")
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "add_collection": "/add",
            "collections": "/all",
            "collection": "/all/<username>",
            "delete": "/delete/<id>",
            "clean": "/clean"
        }
    })


@app.route("/add", methods=['POST'])
def add():
    form = request.form
    c = Collections.new(form)
    c = c.json()
    return nice_json(c)


@app.route('/all')
def all():
    cs = Collections.all()
    cs = [i.json() for i in cs]
    return nice_json(cs)


@app.route("/all/<username>")
def find_by(username):
    try:
        c = Collections.find_by(username=username)
        c = c.json()
        return nice_json(c)
    except:
        raise NotFound

@app.route("/delete")
def delete():
    id = int(request.args.get('id'))
    Collections.delete(id)
    return 'delete success!'


@app.route("/clean")
def clean():
    Collections.clean()
    return "clean done!"


@app.route("/all/<username>/<movieid>")
def collection_movies(username, movieid):
    try:
        # collection_movies = requests.get("http://127.0.0.1:5001/all/{}".format(movieid))
        collection_movies = requests.get("movieservice/all/{}".format(movieid))
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The Movie service is unavailable.")

    if collection_movies.status_code == 404:
        raise NotFound("No movie_info were found for {}".format(movieid))

    collection_movies = collection_movies.json()
    return nice_json(collection_movies)


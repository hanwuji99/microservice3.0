from . import root_dir, nice_json
from flask import Flask,request
from werkzeug.exceptions import NotFound
from database.movies import Movies
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "movies": "/all",
            "movie": "/all/<id>"
        }
    })
@app.route("/add",methods=['POST'])
def add():
    form = request.form
    m = Movies.new(form)
    m = m.json()
    return nice_json(m)

@app.route("/all")
def all():
    ms = Movies.all()
    ms = [i.json() for i in ms]
    return nice_json(ms)

@app.route("/all/<movieid>")
def find_by(movieid):
    try:
        m = Movies.find_by(movieid=movieid)
        m = m.json()
        return nice_json(m)
    except:
        raise NotFound



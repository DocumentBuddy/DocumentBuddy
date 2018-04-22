from flask import Flask, jsonify, abort, request, g, render_template, send_file, send_from_directory,redirect
import sqlite3
import jinja2
import os

from flask_cors import CORS

from api.sqlite import Sqlite


app = Flask(__name__)
CORS(app)
my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('web/'),
])
app.jinja_loader = my_loader
pdfpath = None

def get_documents_by_keyword(keyword, is_like):
    if is_like:
        documents = get_db().select_all_including_keyword(keyword)
    else:
        documents = get_db().select_all_precise_by_keyword(keyword)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects)


def get_documents_by_place(place, is_like):
    if is_like:
        documents = get_db().select_all_including_place(place)
    else:
        documents = get_db().select_all_precise_by_place(place)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects)


def get_documents_by_name(name, is_like):
    if is_like:
        documents = get_db().select_all_including_name(name)
    else:
        documents = get_db().select_all_precise_by_name(name)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects)

@app.route('/')
def hello_world():
    global pdfpath
    print(pdfpath)
    return render_template('index.html',  pdfpath=pdfpath)
    # return '<center><h1>It works!</h1> <br> <h2>Sincerely yours, DocumentBuddy</h2></center>'

@app.route('/exampleData/<path:path>')
def get_examplepdf(path):
    return send_file(os.path.abspath("../exampleData/"+path))


@app.route('/pdf/getid', methods=['GET'])
def get_pdfid():
    global pdfpath
    return jsonify({"path":pdfpath})

@app.route('/pdf/<int:id>', methods=['POST'])
def get_pdf(id):
    global pdfpath
    pdfpath = se_id(int(id))
    return "OK", 200


# Get all documents
@app.route('/database/api/v1.0/documents/', methods=['GET'])
def get_all_documents():
    documents = get_db().select_all('main')
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects)


# Delete :(
@app.route('/database/api/v1.0/documents/delete/all', methods=['GET'])
def delete_all_documents():
    get_db().truncate_database('main')
    return 204


# GET data from exact keyword
@app.route('/database/api/v1.0/keyword/exact/<string:keyword>', methods=['GET'])
def get_documents_by_keyword_exact(keyword: str) -> str:
    return get_documents_by_keyword(keyword, False)


# GET data from like keyword
@app.route('/database/api/v1.0/keyword/like/<string:keyword>', methods=['GET'])
def get_documents_by_keyword_like(keyword):
    return get_documents_by_keyword(keyword, True)


# GET data from exact place (places)
@app.route('/database/api/v1.0/place/exact/<string:place>', methods=['GET'])
def get_documents_by_place_exact(place: str) -> str:
    return get_documents_by_place(place, False)


# GET data from like place (places)
@app.route('/database/api/v1.0/place/like/<string:place>', methods=['GET'])
def get_documents_by_place_like(place: str) -> str:
    return get_documents_by_place(place, True)


# GET data from exact name_entity
@app.route('/database/api/v1.0/name_entity/exact/<string:name_entity>', methods=['GET'])
def get_documents_by_name_exact(name_entity: str) -> str:
    return get_documents_by_name(name_entity, False)


# GET data from like names
@app.route('/database/api/v1.0/name_entity/like/<string:name_entity>', methods=['GET'])
def get_documents_by_name_like(name_entity: str) -> str:
    return get_documents_by_name(name_entity, True)

# GET all keywords
@app.route('/database/api/v1.0/keywords/', methods=['GET'])
def get_all_keywords():
    documents = get_db().select_all('keywords')
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'keyword': document[1]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201


# GET data from many keywords
@app.route('/database/api/v1.0/keywords/many/', methods=['POST'])
def select_keywords():
    if not request.json or 'keywords' not in request.json:
        abort(400)
    data_container = get_db().select_from_keywords(request.json['keywords'])
    json_objects=[]
    for data in data_container:
        print(data)
        json_object = {'id': data[0], 'link': data[1], 'text': data[2], 'doctype': data[3], 'toc':
            data[4], 'author':  data[5], 'pages':  data[6], 'date':  data[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201


# INSERT data on keywords
@app.route('/database/api/v1.0/keywords/insert/', methods=['POST'])
def insert_keywords():
        if not request.json or 'id' not in request.json or 'keywords' not in request.json:
            abort(400)
        try:
            get_db().insert_data_in_keywords(request.json['id'], request.json['keywords'])
        except sqlite3.IntegrityError:
            abort(400)
        json_object = {'id': request.json['id'], 'keywords': request.json['keywords']}
        return jsonify(json_object), 201


# GET all places
@app.route('/database/api/v1.0/places/', methods=['GET'])
def get_all_places():
    documents = get_db().select_all('places')
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'place': document[1]}
        json_objects.append(json_object)
    return jsonify(json_objects)

# GET all name_entities
@app.route('/database/api/v1.0/names/', methods=['GET'])
def get_all_names():
    documents = get_db().select_all('names')
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'name_entity': document[1]}
        json_objects.append(json_object)
    return jsonify(json_objects)

def translate_text(text):
    return str(text.encode("latin-1","ignore"),"latin-1")


def se_id(id: int) -> str:
    print(id)
    data_container = get_db().select_from_id(id)
    json_objects=[]
    for data in data_container:
        return translate_text(data[1])

# GET data from exact author
@app.route('/database/api/v1.0/author/like/<string:author>', methods=['GET'])
def get_data_from_author(author: str)->str:
    documents = get_db().select_like_from_author(author)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3],
                       'toc': document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201


# GET data from like author
@app.route('/database/api/v1.0/doctype/like/<string:doctype>', methods=['GET'])
def get_data_from_doctype(doctype: str)->str:
    documents = get_db().select_like_from_doctype(doctype)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3],
                       'toc': document[4], 'author': document[5], 'pages': document[6], 'date': document[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201


# GET data from ID
@app.route('/database/api/v1.0/id/<int:id>', methods=['GET'])
def select_id(id: int)-> str:
    data_container = get_db().select_from_id(id)
    json_objects=[]
    for data in data_container:
        print(data)
        json_object = {'id': data[0], 'link': data[1], 'text': data[2], 'doctype': data[3], 'toc':
            data[4], 'author':  data[5], 'pages':  data[6], 'date':  data[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201

# GET summary from ID
@app.route('/database/api/v1.0/summary/<int:id>', methods=['GET'])
def select_text_from_id(id: int)-> str:
    data = get_db().select_text_from_id(id)
    json_object = {'summary': data[0]}
    return jsonify(json_object), 201

# GET data from many places
@app.route('/database/api/v1.0/places/many/', methods=['POST'])
def select_places():
    if not request.json or 'places' not in request.json:
        abort(400)
    data_container = get_db().select_from_places(request.json['places'])
    json_objects=[]
    for data in data_container:
        print(data)
        json_object = {'id': data[0], 'link': data[1], 'text': data[2], 'doctype': data[3], 'toc':
            data[4], 'author':  data[5], 'pages':  data[6], 'date':  data[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201

# GET data from many names
@app.route('/database/api/v1.0/name_entity/many/', methods=['POST'])
def select_names():
    if not request.json or 'name_entity' not in request.json:
        abort(400)
    data_container = get_db().select_from_names(request.json['name_entity'])
    json_objects=[]
    for data in data_container:
        print(data)
        json_object = {'id': data[0], 'link': data[1], 'text': data[2], 'doctype': data[3], 'toc':
            data[4], 'author':  data[5], 'pages':  data[6], 'date':  data[7]}
        json_objects.append(json_object)
    return jsonify(json_objects), 201

# INSERT data into main
@app.route('/database/api/v1.0/documents/insert/', methods=['POST'])
def insert_documents():
    if not request.json or 'link' not in request.json or 'text' not in request.json or 'doctype' not in request.json \
            or 'toc' not in request.json or 'author' not in request.json or 'places' not in request.json \
            or 'pages' not in request.json or 'date' not in request.json or 'name_entity' not in request.json:
        abort(400)
    if 'keywords' not in request.json:
        get_db().insert_data_in_main(request.json['link'], request.json['text'], request.json['doctype'],
                                     request.json['toc'], request.json['author'], request.json['name_entity'],
                                     request.json['pages'], request.json['date'], request.json['places'])
        json_object = {'link': request.json['link'],
                       'text': request.json['text'],
                       'doctype': request.json['doctype'],
                       'toc': request.json['toc'],
                       'author':  request.json['author'],
                        'name_entity': request.json['name_entity'],
                       'pages':  request.json['pages'],
                       'date':  request.json['date'],
                       'places':  request.json['places']}
    else:
        keywords = []
        for index in range(0, len(request.json['keywords'])):
            keywords.append(request.json['keywords'][index])
        #print(keywords)
        #print(request.json['link'])
        get_db().insert_data(request.json['link'], keywords, request.json['text'], request.json['doctype'],
                             request.json['toc'], request.json['author'], request.json['places'],
                             request.json['pages'], request.json['date'])
        json_object = {'link': request.json['link'],
                       'text': request.json['text'],
                       'keywords': keywords,
                       'doctype': request.json['doctype'],
                       'toc': request.json['toc'],
                       'author':  request.json['author'],
                       'places':  request.json['places'],
                       'pages':  request.json['pages'],
                       'date':  request.json['date']}
    return jsonify(json_object), 201


@app.route('/<string:path>')
def get_ressources(path):
    return send_file(os.path.abspath("web/"+path))


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = Sqlite()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close_connection()

from flask import Flask, jsonify, abort, request, g

from api.sqlite import Sqlite


app = Flask(__name__)


def get_documents_by_keyword(keyword, is_like):
    if is_like:
        documents = get_db().select_all_including_keyword(keyword)
    else:
        documents = get_db().select_all_precise_by_keyword(keyword)
    if len(documents) == 0:
        abort(404)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'name_entities': document[6], 'pages': document[7], 'date': document[8]}
        json_objects.append(json_object)
    return jsonify(json_objects)


@app.route('/')
def hello_world():
    return '<center><h1>It works!</h1> <br> <h2>Sincerely yours, DocumentBuddy</h2></center>'


@app.route('/database/api/v1.0/documents/', methods=['GET'])
def get_all_documents():
    documents = get_db().select_all('main')
    if len(documents) == 0:
        abort(404)
    json_objects = []
    for document in documents:
        json_object = {'id': document[0], 'link': document[1], 'text': document[2], 'doctype': document[3], 'toc':
            document[4], 'author': document[5], 'name_entities': document[6], 'pages': document[7], 'date': document[8]}
        json_objects.append(json_object)
    return jsonify(json_objects)


@app.route('/database/api/v1.0/documents/delete/all', methods=['GET'])
def delete_all_documents():
    get_db().truncate_database('main')
    return 204


@app.route('/database/api/v1.0/documents/keyword/exact/<string:keyword>', methods=['GET'])
def get_documents_by_keyword_exact(keyword: str) -> str:
    return get_documents_by_keyword(keyword, False)


@app.route('/database/api/v1.0/documents/keyword/like/<string:keyword>', methods=['GET'])
def get_documents_by_keyword_like(keyword):
    return get_documents_by_keyword(keyword, True)


@app.route('/database/api/v1.0/documents/insert/', methods=['POST'])
def insert_documents():
    if not request.json or 'link' not in request.json or 'text' not in request.json or 'doctype' not in request.json:
        abort(400)
    if 'keywords' not in request.json:
        get_db().insert_data_in_main(request.json['link'], request.json['text'], request.json['doctype'])
        json_object = {'link': request.json['link'],
                       'text': request.json['text'],
                       'doctype': request.json['doctype']}
    else:
        keywords = []
        for index in range(0, len(request.json['keywords'])):
            keywords.append(request.json['keywords'][index])
        print(keywords)
        print(request.json['link'])
        get_db().insert_data(request.json['link'], keywords, request.json['text'], request.json['doctype'])
        json_object = {'link': request.json['link'],
                       'text': request.json['text'],
                       'keywords': keywords,
                       'doctype': request.json['doctype']}
    return jsonify(json_object), 201


@app.route('/database/api/v1.0/keywords/', methods=['GET'])
def get_all_keywords():
    documents = get_db().select_all('keywords')
    if len(documents) == 0:
        abort(404)
    json_objects = []
    for document in documents:
        json_object = {'link': document[0], 'keyword': document[1]}
        json_objects.append(json_object)
    return jsonify(json_objects)


@app.route('/database/api/v1.0/keywords/insert/', methods=['POST'])
def insert_keywords():
    if not request.json or 'link' not in request.json or 'keywords' not in request.json:
        abort(400)
    get_db().insert_data_in_keywords(request.json['link'], request.json['keywords'])
    json_object = {'link': request.json['link'], 'keywords': request.json['keywords']}
    return jsonify(json_object), 201


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

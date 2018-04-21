from flask import Flask, jsonify, abort
from sqlite import Sqlite

app = Flask(__name__)


def get_documents_by_keyword(keyword, is_like):
    if is_like:
        documents = sqlite.selectAllIncludingKeyword(keyword)
    else:
        documents = sqlite.selectAllPreciseByKeyword(keyword)
    if len(documents) == 0:
        abort(404)
    json_objects = []
    for document in documents:
        json_object = {'link': document[0], 'text': document[1], 'doctype': document[2]}
        json_objects.append(json_object)
    return jsonify(json_objects)


@app.route('/')
def hello_world():
    return '<center><h1>It works!</h1> <br> <h2>Sincerely yours, DocumentBuddy</h2></center>'


@app.route('/database/api/v1.0/documents/keyword/exact/<string:keyword>', methods=['GET'])
def get_documents(keyword):
    return get_documents_by_keyword(keyword, False)


@app.route('/database/api/v1.0/documents/keyword/like/<string:keyword>', methods=['GET'])
def get_documents(keyword):
    return get_documents_by_keyword(keyword, True)


if __name__ == '__main__':
    sqlite = Sqlite('./example.db')
    app.run()

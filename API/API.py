from flask import Flask, jsonify, abort
from sqlite import Sqlite

app = Flask(__name__)

def get_documents_by_keyword(keyword, isLike):
    if(isLike):
        documents = sqlite.selectAllIncludingKeyword(keyword)
    else:
        documents = sqlite.selectAllPreciseByKeyword(keyword)
    if len(documents) == 0:
        abort(404)
    jsonObjects = []
    for document in documents:
        object = {}
        object['link'] = document[0]
        object['text'] = document[1]
        object['doctype'] = document[2]
        jsonObjects.append(object)
    return jsonify(jsonObjects)


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

from flask import Flask, jsonify, abort
from sqlite import Sqlite

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<center><h1>It works!</h1> <br> <h2>Sincerely yours, DocumentBuddy</h2></center>'


@app.route('/database/api/v1.0/documents/keyword/<string:keyword>', methods=['GET'])
def get_documents(keyword):
    documents = sqlite.selectAllPreciseByKeyword(keyword)
    if len(documents) == 0:
        abort(404)
    json = "["
    for document in documents:
        json = json + {'link': document[0], 'text': document[1], 'doctype': document[2]}
    json = json + "]"
    return jsonify(json)


if __name__ == '__main__':
    sqlite = Sqlite('./example.db')
    app.run()

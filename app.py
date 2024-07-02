from flask import Flask, jsonify, request

import services


app = Flask(__name__)


@app.get('/')
def index():
    return jsonify({'status': 'ok'}), 200


@app.post('/query')
def query_system():
    data = request.json
    response = services.query_with_rag(data=data)
    return jsonify(response)
    

if __name__ == '__main__':
    app.run(debug=True)

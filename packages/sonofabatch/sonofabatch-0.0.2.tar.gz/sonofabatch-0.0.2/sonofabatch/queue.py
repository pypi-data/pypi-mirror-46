from flask import Flask, jsonify
from flask_restful import reqparse
import json

queue = []
app = Flask(__name__)


@app.route('/api/queue/job', methods=['GET'])
def get_job():
    if len(queue) > 0:
        next_item = queue.pop(0)
        return jsonify({
            'job': next_item
        }), 200

    return "", 404


@app.route('/api/queue/job', methods=['PUT'])
def put_job():
    parser = reqparse.RequestParser()
    parser.add_argument('key', type=str, help='Job key')
    args = parser.parse_args()
    queue.append(args['key'])
    return jsonify({
        'status': 'ok'
    }), 201


@app.route('/api/queue/stat', methods=['GET'])
def get_queue_size():
    return jsonify({
        'size': len(queue)
    }), 200


if __name__ == '__main__':
    app.run(debug=True)

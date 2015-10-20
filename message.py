from flask import Flask, jsonify, abort, make_response, request, json
from datetime import datetime

app = Flask(__name__)

messages = [
            {
                'id': 1,
                'sender': u'Gina',
                'message': u'Hello world!!',
                'timestamp': datetime.now(),
                'is_read': False
            },
            {
                'id': 2,
                'sender': u'John',
                'message': u'Hi, I am John',
                'timestamp': datetime.now(),
                'is_read': False
            }
        ]

@app.route('/messages/api/message/all', methods=['GET'])
def get_all_messages():
    return jsonify({ 'messages': messages })


@app.route('/messages/api/message/<int:id>', methods=['GET'])
def get_message(id):
    message = filter(lambda m: m['id'] == id, messages)

    if len(message) == 0:
        abort(404)

    message[0]['is_read'] = True

    return jsonify({ 'messages': message[0] })


@app.route('/messages/api/message', methods=['POST'])
def create_message():

    if not request.json or not 'message' in request.json:
        abort(400)

    if 'message' in request.json and type(request.json['message']) is not unicode:
        abort(400)

    # Get the id of the last message and create the new one
    message = {
        'id': messages[-1]['id'] + 1,
        'sender': request.json['sender'],
        'message': request.json['message'],
        'timestamp': datetime.now(),
        'is_read': False
    }

    messages.append(message)
    return jsonify( {'message': message} ), 201

@app.route('/messages/api/message/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = filter(lambda m: m['id'] == id, messages)

    if len(message) == 0:
        abort(404)

    messages.remove(message[0])
    return jsonify( {'deleted': True} ), 200

@app.route('/messages/api/message/<int:id>', methods=['PUT'])
def edit_message(id):
    message = filter(lambda m: m['id'] == id, messages)

    if len(message) == 0:
        abort(404)

    if not request.json or not 'message' in request.json:
        abort(400)

    if 'message' in request.json and type(request.json['message']) is not unicode:
        abort(400)

    message[0]['message'] = request.json.get('message', message[0]['message'])
    message[0]['is_read'] = False
    message[0]['timestamp'] = datetime.now()


    return jsonify( {'message': message[0]} ), 200


#
# Error handlers
#
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not Found' }), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({ 'error': 'Bad Request' }), 400)

if __name__ == '__main__':
    app.run(debug = True)

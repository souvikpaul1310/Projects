from flask import Flask, jsonify
import random
import string
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
auth_key = None


def generate_key():
    global auth_key
    auth_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
    return auth_key


class GenerateKey(Resource):
    def post(self):
        auth_key = generate_key()
        return jsonify({'auth_key': auth_key})


class GetKey(Resource):
    def get(self):
        global auth_key
        if auth_key:
            return jsonify({'auth_key': auth_key})
        else:
            return jsonify({'error': 'No authentication key provided'}), 400


api.add_resource(GenerateKey, '/generate_key')
api.add_resource(GetKey, '/get_key')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

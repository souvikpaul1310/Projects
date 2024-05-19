import os
from flask import Flask, jsonify, request
import random
import string
from flask_restful import Api, Resource, reqparse

parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app)
auth_key = None

API_KEY = os.getenv('API_KEY')


def generate_key():
    global auth_key
    auth_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
    return auth_key


def verify_api_key(request):
    api_key = request.headers.get('x-api-key')
    return api_key == API_KEY
    

class GenerateKey(Resource):
    def post(self):
        #args = parser.parse_args()
        if not verify_api_key(request):
            return jsonify({'error': 'Unauthorized', 'message': 'Invalid or missing API key'}), 401
        
        auth_key = generate_key()
        return jsonify({'auth_key': auth_key})


class GetKey(Resource):
    def get(self):
        #args = parser.parse_args()
        if not verify_api_key(request):
            return jsonify({'error': 'Unauthorized', 'message': 'Invalid or missing API key'}), 401
            
        global auth_key
        if auth_key:
            return jsonify({'auth_key': auth_key})
        else:
            return jsonify({'error': 'Not Found', 'message': 'No authentication key has been generated'}), 404


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested URL was not found on the server'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed', 'message': 'The method is not allowed for the requested URL'}), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'An internal server error occurred'}), 500
    
api.add_resource(GenerateKey, '/generate_key')
api.add_resource(GetKey, '/get_key')


from flask import Flask, jsonify, request, make_response
import secrets
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
auth_key = None


def generate_key():
    global auth_key
    auth_key = secrets.token_hex(16)
    return auth_key
    

class GenerateKey(Resource):
    def get(self):
            return jsonify({'error': 'Unauthorized', 'message': 'Invalid or missing API key'}), 401
        
        auth_key = generate_key()
        return make_response(auth_key, 200)


class GetKey(Resource):
    def get(self):
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

from flask import Flask, jsonify, abort
import random
import string
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<USERNAME>:<PASSWORD>@/<DATABASE_NAME>?unix_socket=/cloudsql/<CONNECTION_NAME>'
db = SQLAlchemy(app)
api = Api(app)

#db model for keys
class AuthKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy=True))

#db model for user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)

#db model for arduino device
class ArduinoDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(17), unique=True)  # MAC address
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('devices', lazy=True))


class GenerateKey(Resource):            #RESTful API call to generate key
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")

        existing_key = AuthKey.query.filter_by(user_id=user_id).first()
        if existing_key:
            existing_key.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            db.session.commit()
            return jsonify({'auth_key': existing_key.key}), 200
        else:
            auth_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            auth_key = AuthKey(key=auth_code, user=user)
            db.session.add(auth_key)
            db.session.commit()
            return jsonify({'auth_key': auth_code}), 201


class GetAuthCode(Resource):                #RESTful API call to get the authkey to the arduino device
    def get(self, user_id, mac_address):
        if not mac_address:
            abort(400, description="MAC address is required")

        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")

        device = ArduinoDevice.query.filter_by(mac_address=mac_address, user_id=user_id).first()
        if not device:
            abort(403, description="Unauthorized device")

        auth_key = AuthKey.query.filter_by(user_id=user_id).first()
        if not auth_key:
            abort(404, description="Auth key not found for this user")

        return jsonify({'auth_key': auth_key.key}), 200


api.add_resource(GenerateKey, '/generate_key/<int:user_id>')
api.add_resource(GetAuthCode, '/get_auth_code/<int:user_id>/<mac_address>')


@app.errorhandler(400)
def bad_request(error):      #Bad request handling
    return jsonify({'error': 'Bad request', 'message': error.description}), 400


@app.errorhandler(403)
def forbidden(error):      #Forbidden request handling
    return jsonify({'error': 'Forbidden', 'message': error.description}), 403


@app.errorhandler(404)
def not_found(error):        #Not-found error handling
    return jsonify({'error': 'Not found', 'message': error.description}), 404


@app.errorhandler(500)
def internal_error(error):        #Internal Error Handling
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}, error), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

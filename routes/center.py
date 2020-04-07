import datetime
import json
import jwt
from functools import wraps
from flask import current_app as app
from flask import jsonify, request, Response

from models import Center, AccessRequest


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            secrets = jwt.decode(token, app.config['SECRET_KEY'])
            return f(caller_id=secrets['center_id'], *args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401

    return wrapper


@app.route('/centers', methods=['GET'])
def get_centers():
    return jsonify({'centers': Center.get_all_centers()})


@app.route('/centers/<int:id>')
def get_center_by_id(id):
    center = Center.get_center_by_id(id)
    return jsonify(center)


@app.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    if Center.is_valid_object(request_data):
        try:
            Center.add_center(request_data['login'], request_data['password'], request_data['address'])
            response = Response('', status=201, mimetype='application/json')
            return response
        except TypeError as te:
            return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')
    else:
        invalid_obj = {
            'error': "Valid Center must contain: login, password and address"
        }
        response = Response(json.dumps(invalid_obj), 400)
        return response


@app.route('/login', methods=['GET'])  # Should be POST, but in task is listed as GET
def get_token():
    login = request.args.get('login')
    password = request.args.get('password')
    if Center.valid_credentials(login, password):
        center = Center.query.filter_by(_login=login, _password=password).first()
        AccessRequest.add_access_request(center.id)
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        token = jwt.encode({'exp': expiration_date, 'center_id': center.id}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return jsonify({'error': "Not valid login and password"}), 400


@app.route('/accesses')
def get_all_accesses():
    return jsonify(AccessRequest.get_all_access_requests())
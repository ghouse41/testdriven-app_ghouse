from project import db
from project.api.models import User
from functools import wraps
from flask import request, jsonify

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)
    return decorated_function

def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin

def add_admin(username, email, password):
    user = User(
        username=username, email=email,
        password=password, admin=True
    )
    db.session.add(user)
    db.session.commit()
    return user
from flask import Blueprint, jsonify, request, redirect, flash, render_template
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt
from project.api.utils import authenticate
from project.api.email import send_password_reset_email
from project.api.forms import ResetPasswordForm

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully registered.'
            response_object['auth_token'] = auth_token.decode()
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400

@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['auth_token'] = auth_token.decode()
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception as e:
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500

@auth_blueprint.route('/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200

@auth_blueprint.route('/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'message': 'success',
        'data': user.to_json()
    }
    return jsonify(response_object), 200

@auth_blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')    
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
            response_object['status'] = 'success'
            response_object['message'] = 'Check your email for the instructions to reset your password.'
            return jsonify(response_object), 200
        else:
            response_object['message'] = 'Invalid User'
            return jsonify(response_object), 404
    except Exception as e:
        response_object['message'] = e
        return jsonify(response_object), 500

@auth_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token): 
    try:
        user = User.verify_reset_password_token(token)
        if not user:
            return redirect("http://localhost/")

        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been reset.')
            return redirect("http://localhost/")
        return render_template('auth/reset_password.html',form=form)
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return redirect("http://localhost/")
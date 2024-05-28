from flask import Blueprint, url_for, render_template, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_wtf.csrf import generate_csrf

from 아맞다 import db
from 아맞다.forms import UserCreateForm, UserLoginForm
from 아맞다.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    data = request.json
    if request.method == 'POST':
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return jsonify({'error': 'User already exists'})
        else:
            email = User.query.filter_by(email=data['email']).first()
            if email:
                return jsonify({'error': 'Email already exists'})
            else:                     
                user = User(username=data['username'],
                            password=generate_password_hash(data['password1']),
                            email=data['email'])
                db.session.add(user)
                db.session.commit()
                return jsonify({'success': 'User created successfully'})
    return jsonify({'error': 'Invalid data or request method'})

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    data = request.json
    if request.method == 'POST':
        error = None
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
            return jsonify({'error':error})
        elif not check_password_hash(user.password, data['password']):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return jsonify({'success': 'User login successfully'})
        else:
            return jsonify({'error':error})

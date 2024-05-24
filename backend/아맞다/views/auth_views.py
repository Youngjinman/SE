from flask import Blueprint, url_for, render_template, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from 아맞다 import db
from 아맞다.forms import UserCreateForm, UserLoginForm
from 아맞다.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    data = request.json
    form = UserCreateForm(data=data)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return jsonify({'error': 'User already exists'})
        else:
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                return jsonify({'error': 'Email already exists'})
            else:                     
                user = User(username=form.username.data,
                            password=generate_password_hash(form.password1.data),
                            email=form.email.data)
                db.session.add(user)
                db.session.commit()
                return jsonify({'success': 'User created successfully'})
    return jsonify({'error': 'Invalid data or request method'})

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    data = request.json
    form = UserLoginForm(data=data)
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
            return jsonify({'error':error})
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return jsonify({'success': 'User login successfully'})
        else:
            return jsonify({'error':error})
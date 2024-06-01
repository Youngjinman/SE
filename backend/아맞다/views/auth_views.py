from flask import Blueprint, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_wtf.csrf import generate_csrf
import secrets
from flask_mail import Message
from flask import make_response
from datetime import datetime, timedelta
from flask_session import Session

from 아맞다 import db
from 아맞다.forms import UserCreateForm, UserLoginForm
from 아맞다.models import User
from .. import mail
import config

bp = Blueprint('auth', __name__, url_prefix='/auth')

user2code = {}

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    data = request.json.get('data')
    email = data.get('email')
    user_verification = data.get('verification_code')
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')
    #print(session.get('verification_code')

    if user_verification != user2code[email]: #session.get('verification_code'):
        return jsonify({'error': 'verification unmatched'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Check if passwords match
    if password1 != password2:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Create new user
    new_user = User(username=username, email=email, password=generate_password_hash(password1))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/send-verification-email/', methods=['POST'])
def send_verification_email():
    data = request.json.get('data')
    email = data.get('email')

    if '@' not in email:
        return jsonify({'error': 'email form invalid'}), 400
        
    domain = email.split('@')[1]
    if domain != 'skku.edu' and domain != 'g.skku.edu':
        return jsonify({'error': 'email should skku'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already exists'}), 400
    
    # Generate verification code
    verification_code = generate_verification_code()
    # session['verification_code'] = verification_code
    user2code[email] = verification_code
    # Send verification email
    send_verification_email(email, verification_code)

    return jsonify({'message': 'Verification email sent successfully'}), 200

from flask import make_response

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    data = request.json.get('data')
    if request.method == 'POST':
        error = None
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
            return jsonify({'error':error})
        elif not check_password_hash(user.password, data['password']):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            # session.clear()
            #session['user_id'] = user.id
            #print(session.get('user_id'))

          #  print(server_sessionsession)
            
            # 쿠키 설정
            response = jsonify({'success': 'User login successfully', "userid": user.id})
            # response = make_response(response)
            # response.set_cookie('user_id', str(user.id))
            return response, 201
        else:
            return jsonify({'error':error}), 400

def generate_verification_code():
    # Generate a random 6-digit verification code
    return ''.join(secrets.choice('0123456789') for i in range(6))

def send_verification_email(email, verification_code):
    # Create a message object with sender, recipients, subject, and body
    msg = Message(subject="Verify Your Email",sender=config.MAIL_USERNAME, recipients=[email])
    msg.body = f"Your verification code is: {verification_code}"

    # Send the email
    mail.send(msg)

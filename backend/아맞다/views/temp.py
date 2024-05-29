from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Api, Resource
from 아맞다 import db, mail  # 아맞다 모듈에서 db와 mail을 가져옵니다.
from 아맞다.forms import UserCreateForm, UserLoginForm
from 아맞다.models import User
import config
import secrets

bp = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(bp, version='1.0', title='Auth API', description='signup, login, email API')

class Signup(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        user_verification = data.get('verification_code')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if user_verification != session.get('verification_code'):
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

class SendVerificationEmail(Resource):
    def post(self):
        data = request.json
        email = data.get('email')

        if '@' not in email:
            return jsonify({'error': 'email form invalid'}), 400
            
        domain = email.split('@')[1]
        if domain != 'skku.edu':
            return jsonify({'error': 'email should skku'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'email already exists'}), 400
        
        # Generate verification code
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code
        print(verification_code)

        # Send verification email
        send_verification_email(email, verification_code)

        return jsonify({'message': 'Verification email sent successfully'}), 200

class Login(Resource):
    def post(self):
        data = request.json
        error = None
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
            return jsonify({'error': error})
        elif not check_password_hash(user.password, data['password']):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return jsonify({'success': 'User login successfully'})
        else:
            return jsonify({'error': error})

def generate_verification_code():
    # Generate a random 6-digit verification code
    return ''.join(secrets.choice('0123456789') for i in range(6))

def send_verification_email(email, verification_code):
    # Create a message object with sender, recipients, subject, and body
    msg = Message(subject="Verify Your Email", sender=config.MAIL_USERNAME, recipients=[email])
    msg.body = f"Your verification code is: {verification_code}"

    # Send the email
    mail.send(msg)

api.add_resource(Signup, '/signup/')
api.add_resource(SendVerificationEmail, '/send-verification-email/')
api.add_resource(Login, '/login/')

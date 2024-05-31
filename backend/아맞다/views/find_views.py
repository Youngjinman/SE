from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from 아맞다.models import FindingLostItems
from 아맞다 import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from 아맞다.models import User

bp = Blueprint('find', __name__, url_prefix='/find')

@bp.route('/register/', methods=['GET', 'POST'])
def step3():
    # user_id = request.cookies.get('user_id')
    # print(f"user id: {user_id}")
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'user not login'}), 400
    user = User.query.filter_by(id=user_id).first() 
    # Store the form data in session
    item = request.form.get('item')
    if item is None:
        return jsonify({'error': 'item field necessary'}), 400
    if 'photo' in request.files:
        # 'photo' 필드가 없다면 pass
        photo = request.files['photo']
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join('uploads', photo_filename)
        photo.save(photo_path)
    else:
        photo_filename = None
    manufacturer = request.form.get('manufacturer','')
    color = request.form.get('color','')
    location = request.form.get('location','')
    time = request.form.get('time','2000-01-01 12:00')
    contents = request.form.get('contents', '')
    reward = request.form.get('reward', 0)

    # Save all the collected data to the database
    lost_item = FindingLostItems(
        user_id=user_id,
        item=item,
        color=color,
        contents=contents,
        manufacturer=manufacturer,
        location=location,
        time=datetime.strptime(time, '%Y-%m-%d %H:%M'),
        photo=photo_filename,
        reward=reward
    )
    db.session.add(lost_item)
    db.session.commit()
    
    # Clear the session data
    #session.clear()
    
    return jsonify({'success': 'lost item registered successfully', 'total reward':user.reward}), 201

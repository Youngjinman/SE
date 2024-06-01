from flask import Blueprint, request, jsonify
from 아맞다 import db  # 아맞다 모듈에서 db와 mail을 가져옵니다.
from 아맞다.models import *
import editdistance

bp = Blueprint('find_list', __name__, url_prefix='/profile')

@bp.route('/find_list/', methods=['GET']) #내가 잃어버린 물건 리스트
def find_list():
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'user not login'}), 400

    rows = FindingLostItems.query.filter_by(user_id=user_id).all()

    result = [{'find_id' : row.find_id, 'item': row.item, 'color': row.color, 'contents' : row.contents, 'manufacturer' : row.manufacturer, 'photo' : row.photo, 'reward' : row.reward, 'location' : row.location, 'time' : row.time, 'is_found' : row.is_found} for row in rows]
    return jsonify(result)

@bp.route('/report_list/', methods=['GET']) #내가 찾은 물건 리스트
def report_list():
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'user not login'}), 400

    rows = ReportLostItem.query.filter_by(user_id=user_id).all()

    result = [{'report_id' : row.report_id, 'item': row.item, 'color': row.color, 'contents' : row.contents, 'manufacturer' : row.manufacturer, 'photo' : row.photo, 'location' : row.location, 'time' : row.time, 'is_found' : row.is_found} for row in rows]
    return jsonify(result)

@bp.route('/find_list/<int:find_id>', methods=['GET']) #내가 잃어버린 물건의 find_id를 url에 넣어주셔야합니다.
def recommend(find_id):
    lost_item = FindingLostItems.query.filter_by(find_id=find_id).first()
    item = lost_item.item
    time = lost_item.time
    color = lost_item.color
    contents = lost_item.contents
    manufacturer = lost_item.manufacturer
    location = lost_item.location


    rows = ReportLostItem.query.filter_by(item=item).all()
    recommend_list = []
    candidates = [{'report_id' : row.report_id, 'item' : row.item, 'time' : row.time, 'color' : row.color, 'contents' : row.contents, 'manufacturer' : row.manufacturer, 'location' : row.location}for row in rows]
    for candidate in candidates:
        if abs(candidate['time'] - time).days > 5:
            continue
        if editdistance.eval(candidate['color'], color) > 1:
            continue
        if editdistance.eval(candidate['manufacturer'], manufacturer) > 3:
            continue
        if editdistance.eval(candidate['location'], location) > 3:
            continue
        candidate['edidistance'] = editdistance.eval(candidate['contents'], contents)
        recommend_list.append(candidate)
    
    recommend_list = sorted(recommend_list, key=lambda x: x['edidistance'])
    return recommend_list
from 아맞다 import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reward = db.Column(db.Integer, default=0)
    
class ReportLostItem(db.Model):
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255))
    contents = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    location_of_discovery = db.Column(db.String(255))
    time_of_discovery = db.Column(db.DateTime)
    photo = db.Column(db.String(255))
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class FindingLostItems(db.Model):
    find_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255))
    contents = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    location_of_discovery = db.Column(db.String(255))
    time_of_discovery = db.Column(db.DateTime)
    photo = db.Column(db.String(255))
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    reward = db.Column(db.Integer, default=0)
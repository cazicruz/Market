from shop import db
from datetime import datetime
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20),unique=False, nullable=False)
    lname = db.Column(db.String(20), unique=False,nullable=False)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    address = db.Column(db.String(50),nullable=True)
    state = db.Column(db.String(50),nullable=True)
    password = db.Column(db.String(80), nullable=False)
    profile_img = db.Column(db.String(180), nullable=True, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)





    
#db.create_all()
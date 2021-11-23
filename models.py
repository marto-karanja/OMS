from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    mobile = db.Column(db.String(50))
    gender = db.Column(db.String(100))
    account_type =  db.Column(db.String(100))
    branch = db.Column(db.String(50))




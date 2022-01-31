import enum

from flask_login import UserMixin
from . import db

class TransactionType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
class TransactionMethod(enum.Enum):
    CASH = "Cash"
    MPESA = "M-pesa"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"



class AccountType(enum.Enum):
    EMPLOYEE = "1"
    CUSTOMER = "0"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_type = db.Column(db.Enum(AccountType))
    customers = db.relationship('Customers', backref='user', uselist = False, lazy=True)
    transactions = db.relationship('Transactions', backref='transactions', lazy=True)

    

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    date_of_birth = db.Column(db.DateTime)
    mobile = db.Column(db.Integer, unique = True)
    gender = db.Column(db.String(100))
    account_type =  db.Column(db.String(100))
    branch = db.Column(db.String(50))
    bank_balance = db.Column(db.Float(precision=2), default = 0)
    transactions = db.relationship('Transactions', backref='customer', lazy=True)

    def __repr__(self):
        return f"{self.name}:{self.id}"

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float(precision=2))
    transaction_identifier = db.Column(db.String(100))
    transaction_type = db.Column(db.Enum(TransactionType))
    transaction_time = db.Column(db.DateTime)
    transaction_method = db.Column(db.Enum(TransactionMethod))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
        nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))





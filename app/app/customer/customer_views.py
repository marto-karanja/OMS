import os
import datetime
from time import time

from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import session
from flask import current_app
from flask_login import login_required, current_user
from flask import Markup
from dateutil.parser import parse
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from flask import send_from_directory

from flask_sqlalchemy import SQLAlchemy
from app.models import BiddingOrders, CompletedOrders, CurrentOrders, EducationLevel, FileOrders, OrderTransactions, Orders, User, Customers, Transactions, TransactionType, TransactionMethod, AccountType, EnglishCountry, Person, Status, Orders, Bids, Order_type, Messages, Department, ThreadStatus, ReadStatus
from app import db
from app.app.admin.admin_views import find_time_difference



customer = Blueprint('customer', __name__)

@customer.route('/customer_dashboard', methods=["GET", "POST"])
#@login_required
def dashboard():
    orders = Orders.query.all()
    for order in orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("client/index.html", orders = orders)
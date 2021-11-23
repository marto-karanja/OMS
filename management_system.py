import os

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import flash
from flask_login import login_required


from .models import Customers
from . import db

from flask_sqlalchemy import SQLAlchemy

admin = Blueprint('admin', __name__)

#-------------------------------------------------------------------------

@admin.route('/', methods=["GET", "POST"])
def home():
    return render_template("main_index.html")

#-------------------------------------------------------------------------------------
@admin.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("admin/index.html")

    
#-------------------------------------------------------------------------------------
@admin.route('/add_customer', methods=["GET", "POST"])
@login_required
def add_customer():
    customer = None
    
    # check if form has been filled
    if request.form:
        name = request.form.get("first_name") + " " + request.form.get("last_name")
        email = request.form.get("email")
        date_of_birth = datetime.strptime(request.form.get("date_of_birth"), '%Y-%M-%d')
        phone = request.form.get("phone")
        gender = request.form.get("gender")
        account_type = request.form.get("account_type")
        branch = request.form.get("branch")

        # create customer object to store in database
        customer = Customers (name = name, email = email, date_of_birth = date_of_birth, mobile = phone, gender = gender, account_type = account_type, branch = branch)

        try:
            db.session.add(customer)
            db.session.commit()
        except Exception as e:
            # for resetting non-commited .add()
            db.session.rollback()
            db.session.flush()
            print("Failed to add customer")
            flash('Database Error: Failed to add customer')
            print(e)
        else:
            # on successful saving
            flash('Customer was added successfully')

    # Fetch all customers 
    customers = Customers.query.all()
    return render_template("admin/add_customer.html", customers = customers)


#--------------------------------------------------------------------
@admin.route('/update_customer', methods=["GET", "POST"])
@login_required
def update_customer():
    return render_template("admin/update_customer.html")

#--------------------------------------------------------------------
@admin.route('/view_customers', methods=["GET", "POST"])
@login_required
def view_customers():
    # Fetch all customers 
    customers = Customers.query.all()
    return render_template("admin/view_customers.html", customers = customers)

#--------------------------------------------------------------------
@admin.route('/view_balances', methods=["GET", "POST"])
@login_required
def view_balances():
    return render_template("admin/view_balances.html")

#--------------------------------------------------------------------
@admin.route('/view_deposits', methods=["GET", "POST"])
@login_required
def view_deposits():
    return render_template("admin/view_deposits.html")

#--------------------------------------------------------------------
@admin.route('/add_deposits', methods=["GET", "POST"])
@login_required
def add_deposits():
    return render_template("admin/add_deposits.html")

#--------------------------------------------------------------------
@admin.route('/process_withdraw', methods=["GET", "POST"])
@login_required
def process_withdraw():
    return render_template("admin/process_withdraw.html")



#-------------------------------------------------------------------------
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)"""
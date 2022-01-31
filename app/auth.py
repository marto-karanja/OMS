# auth.py

from re import A
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Customers, User, AccountType
from .emails import send_user_signup_mail
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("pages/login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('(Incorrect password or email).Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    session['user_id'] = user.id
    # check if customer is an employee or customer user
    if user.user_type == AccountType.EMPLOYEE:
        return redirect(url_for('admin.dashboard'))
    elif user.user_type == AccountType.CUSTOMER:
        return redirect(url_for ('customer.dashboard'))


@auth.route('/register')
def signup():
    return render_template("pages/register.html")

@auth.route('/register', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), user_type = AccountType.EMPLOYEE)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    send_user_signup_mail(new_user.email, name)

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.home'))
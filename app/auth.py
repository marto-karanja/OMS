# auth.py

from re import A
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Customers, User, AccountType
from .emails import send_user_signup_mail
from .forms import LoginForm, RegisterForm
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.is_submitted():
         if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            remember = True if form.remember.data  else False

            # check if user actually exists
            # take the user supplied password, hash it, and compare it to the hashed password in database
            if not user or not check_password_hash(user.password, password): 
                form.email.errors.append('Incorrect password or email.Please check your login details and try again.')
                return render_template("pages/writergigs_login.html", login_form = form) #reload the page

            # if the above check passes, then we know the user has the right credentials
            login_user(user, remember=remember)
            session['user_id'] = user.id
            session['name'] = user.name
            session['email'] = user.email
            # check if customer is an employee or customer user
            print (user.user_type.value)
            if user.user_type.value == AccountType.ADMIN.value:
                print("admin")
                return redirect(url_for('admin.dashboard'))
            if user.user_type.value == AccountType.EDITOR.value:
                print("editor")
                return redirect(url_for('admin.dashboard'))
            elif user.user_type.value == AccountType.WRITER.value:
                print("writer")
                return redirect(url_for('writer.dashboard'))
    return render_template("pages/writergigs_login.html", login_form = form)


#----------------------------------------------------------------------------------------------

@auth.route('/register', methods=['POST', 'GET'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        

        #user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        # change to flask form validation
        """if user: 
            # if a user is found, we want to redirect back to signup page so user can try again  
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))"""

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), user_type = AccountType.EDITOR)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        #send_user_signup_mail(new_user.email, name)

        return redirect(url_for('auth.login'))
    else:
        return render_template("pages/writergigs_register.html", register_form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.home'))
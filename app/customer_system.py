import os

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import flash
from flask import session
from flask_login import login_required



from .models import TransactionMethod, User, Customers, Transactions, TransactionType, TransactionMethod
from .forms import DepositForm, WithdrawForm, CashDepositForm, CustomerDepositForm
from . import db
from .emails import send_message, send_admin_message, send_customer_message
from .mpesa import send_money_request

from flask_sqlalchemy import SQLAlchemy

customer = Blueprint('customer', __name__)


#------------------------------------------------------------------


@customer.route('/customer_dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    # fetch customer balance
    #user = User.query.filter_by(id= session['user_id'])
    customer = Customers.query.filter_by( user_id = session['user_id'] ).first()
    return render_template("customer/index.html", customer = customer, TransactionType = TransactionType)

@customer.route('/mpesa', methods=["GET", "POST"])
def mpesa_process():
    # fetch customer balance

    return "success"

#---------------------------------------------------------------------
@customer.route('/customer_add_deposits', methods=["GET", "POST"])
@login_required
def add_deposits():
    # fetch customer balance

    form = CashDepositForm()
    customer = Customers.query.filter_by( user_id = session['user_id'] ).first()
    if form.validate_on_submit():
        amount = form.amount.data
        transaction_time = datetime.now()
        transaction = Transactions(amount = amount, transaction_type = TransactionType.DEBIT.name, transaction_time = transaction_time, transaction_method = form.payment_method.data)
        # update customer balance
        customer.bank_balance = customer.bank_balance + form.amount.data
        # add transaction to customer
        customer.transactions.append(transaction)

        # save transaction in database
        try:
            db.session.add(customer)
            db.session.commit()
        except Exception as e:
            # for resetting non-commited .add()
            db.session.rollback()
            db.session.flush()
            print("Failed to add transaction")
            flash('Database Error: Failed to process the deposit due to an unexpected error')
            print(e)
        else:
            # on successful saving
            flash('Deposit was completed successfully')
            # send email notifications
            send_admin_message(transaction_subject = "[MIFS]:Successful Deposit", transaction_message = f'An Cash deposit transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')
            send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful Deposit", transaction_message = f'Your Cash Deposit of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )
    return render_template("customer/add_deposits.html", form=form, customer_details = customer)

#------------------------------------------------------------------------


@customer.route('/customer_process_withdraw', methods=["GET", "POST"])
@login_required
def process_withdraw():
    # fetch customer balance

    form = WithdrawForm()
    customer = Customers.query.filter_by( user_id = session['user_id'] ).first()
    if form.validate_on_submit():
        transaction_time = datetime.now()
        transaction = Transactions(amount = form.amount.data, transaction_type = TransactionType.DEBIT.name,transaction_time = transaction_time , transaction_method = form.payment_method.data)
        # update customer balance
        amount = form.amount.data
        if amount <= customer.bank_balance:
                
            customer.bank_balance = customer.bank_balance - form.amount.data
            # add transaction to customer
            customer.transactions.append(transaction)

            # save transaction in database
            try:
                db.session.add(customer)
                db.session.commit()
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("Failed to add transaction")
                flash('Database Error: Failed to process the deposit due to an unexpected error')
                print(e)
            else:
                # on successful saving
                flash('Withdraw was completed successfully')
                send_admin_message(transaction_subject = "[MIFS]:Successful Withdrawal", transaction_message = f'A transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')
                send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful Withdrawal", transaction_message = f'Your withdrawal of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )
        else:
            flash("You cannot withdraw an amount greater than your balance")

    return render_template("customer/process_withdraw.html", form=form, customer_details = customer)

#---------------------------------------------------------------------
@customer.route('/customer_add_mpesa_deposits', methods=["GET", "POST"])
@login_required
def add_mpesa_deposits():
    # fetch customer balance

    customer = Customers.query.filter_by( user_id = session['user_id'] ).first()

    form = CustomerDepositForm(name = customer.user.name, balance = customer.bank_balance, phone_number = customer.mobile, customer_id = customer.id)
    
    if form.validate_on_submit():
        # send mpesa confirmation prompt
        amount = form.amount.data
        phone_number = form.phone_number.data
        transaction_time = datetime.now()
        send_money_request(amount, phone_number)
        transaction = Transactions(amount = amount, transaction_type = TransactionType.DEBIT.name, transaction_time = transaction_time, transaction_method = TransactionMethod.MPESA.name)
        # update customer balance
        customer.bank_balance = customer.bank_balance + form.amount.data
        # add transaction to customer
        customer.transactions.append(transaction)

        # save transaction in database
        try:
            db.session.add(customer)
            db.session.commit()
        except Exception as e:
            # for resetting non-commited .add()
            db.session.rollback()
            db.session.flush()
            print("Failed to add transaction")
            flash('Database Error: Failed to process the deposit due to an unexpected error')
            print(e)
        else:
            # on successful saving
            flash('Transaction Pending..Waiting for M-Pesa Confirmation')

            # send email notifications
            send_admin_message(transaction_subject = "[MIFS]:Successful M-PESA Deposit", transaction_message = f'An M-PESA transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')
            send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful M-PESA Deposit", transaction_message = f'Your M-Pesa Deposit of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )

    return render_template("customer/add_mpesa_deposits.html", deposit_form=form, customer_details = customer)

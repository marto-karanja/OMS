import os

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import flash
from flask_login import login_required
from werkzeug.security import generate_password_hash



from .models import User, Customers, Transactions, TransactionType, TransactionMethod, AccountType
from . import db
from .emails import send_message, send_admin_message, send_customer_message
from .forms import DepositForm, LoginForm
from .mpesa import send_money_request


from flask_sqlalchemy import SQLAlchemy

admin = Blueprint('admin', __name__)

#-------------------------------------------------------------------------

@admin.route('/', methods=["GET", "POST"])
def home():
    form = LoginForm()

    return render_template("pages/writergigs_login.html", login_form = form)

#-------------------------------------------------------------------------------------
@admin.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    #print("Call sending message function")
    #send_message()
    #transactions = Transactions.query.all()
    return render_template("admin/editor/editor_dashboard.html")

    
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
        # create user object first
        password = "incorrect"
        customer = Customers (date_of_birth = date_of_birth, mobile = phone, gender = gender, account_type = account_type, branch = branch)
        user = User(name= name, email = email, password=generate_password_hash(password, method='sha256'), user_type = AccountType.CUSTOMER, customers = customer)

        try:
            db.session.add(user)
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
    customers = Customers.query.all()
    return render_template("admin/view_balances.html", customers = customers)

#-----------------------------------------------------------0---------
@admin.route('/view_deposits', methods=["GET", "POST"])
@login_required
def view_deposits():
    deposits = Transactions.query.filter_by(transaction_type = TransactionType.DEBIT)
    return render_template("admin/view_deposits.html", deposits = deposits)



#-----------------------------------------------------------0---------
@admin.route('/view_withdraws', methods=["GET", "POST"])
@login_required
def view_withdraws():
    withdraws = Transactions.query.filter_by(transaction_type = TransactionType.CREDIT)
    return render_template("admin/view_withdraws.html", withdraws = withdraws)



#--------------------------------------------------------------------
@admin.route('/add_deposits', methods=["GET", "POST"])
@login_required
def add_deposits():
    # get form data
    # create objects and store them
    if request.form:
        customer_id = request.form.get("customer_id")
        amount = float(request.form.get("amount"))
        transaction_time = datetime.now()
        if amount > 0:
            # create customer object
            customer = Customers.query.get(customer_id)
            transaction = Transactions(amount = amount, transaction_type = TransactionType.DEBIT.name,transaction_method = TransactionMethod.CASH.name, transaction_time = datetime.now())
            customer.bank_balance = customer.bank_balance + amount
            # add transactions as a child reference of the customer table
            customer.transactions.append(transaction)


            try:
                db.session.add(customer)
                db.session.commit()
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("Failed to add customer")
                flash('Database Error: Failed to process transaction')
                print(e)
            else:
                # on successful saving
                flash('Transaction was added successfully')
                                # send emails
                send_admin_message(transaction_subject = "[MIFS]:Successful Deposit", transaction_message = f'A Cash deposit transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')
                send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful Deposit", transaction_message = f'Your Cash Deposit of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )
        else:
            flash("Amount has to be greater than zero")



        # return updated customer details
        customer_id = request.form.get("customer_id")
        # fetch customer by ID/ primary key
        customer = Customers.query.get(customer_id) 
        # return updated customer details
        return render_template("admin/add_deposits.html", customer_details = customer)
    else:
        return render_template("admin/add_deposits.html")



#--------------------------------------------------------------------
@admin.route('/process_withdraw', methods=["GET", "POST"])
@login_required
def process_withdraw():
    # get form data
    # create objects and store them
    if request.form:
        customer_id = request.form.get("customer_id")
        amount = float(request.form.get("amount"))
        transaction_time = datetime.now()
        if amount > 0:
            # create customer object
            customer = Customers.query.get(customer_id)
            transaction = Transactions(amount = amount, transaction_type = TransactionType.CREDIT.name,transaction_method = TransactionMethod.CASH.name, transaction_time = datetime.now())
            balance = customer.bank_balance - amount
            if balance > 0:
                customer.bank_balance = balance
                # add transactions as a child reference of the customer table
                customer.transactions.append(transaction)


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
                    flash('Withdraw was completed successfully')
                    send_admin_message(transaction_subject = "[MIFS]:Successful Withdrawal", transaction_message = f'A transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')


                    send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful Withdrawal", transaction_message = f'Your withdrawal of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )
            else:
                    flash("You cannot withdraw an amount greater than your balance")
        else:
            flash("Balance has to be greater than zero")



        # return updated customer details
        customer_id = request.form.get("customer_id")
        # fetch customer by ID/ primary key
        customer = Customers.query.get(customer_id) 
        # return updated customer details
        return render_template("admin/process_withdraw.html", customer_details = customer)
    else:
        return render_template("admin/process_withdraw.html")
#-----------------------------------------------------
@admin.route('/find_customer_deposit', methods = ["GET"])
@login_required
def find_customer_deposit():
    
    customer_id = request.args.get("customer_id")
    # fetch customer by ID/ primary key
    customer = Customers.query.get(customer_id)

    if customer:
        #return balance and customer
        return render_template("admin/add_deposits.html", customer_details = customer)
    else:
        flash("No Such Customer was found")
        return render_template("admin/add_deposits.html")
        # return template pre-populated


@admin.route('/find_customer_withdraw', methods = ["GET"])
@login_required
def find_customer_withdraw():
    
    customer_id = request.args.get("customer_id")
    # fetch customer by ID/ primary key
    customer = Customers.query.get(customer_id)

    if customer:
        #return balance and customer
        return render_template("admin/process_withdraw.html", customer_details = customer)
    else:
        flash("No Such Customer was found")
        return render_template("admin/process_withdraw.html")
        # return template pre-populated



#------------------------------------------------------------------------
@admin.route('/mpesa_withdrawal', methods = ['GET', 'POST'])
@login_required
def process_mpesa_withdraw():
    pass



#------------------------------------------------------------------------
@admin.route('/mpesa_deposit', methods = ['GET', 'POST'])
@login_required
def process_mpesa_deposit():
    deposit_form = DepositForm()
    
    if deposit_form.validate_on_submit():
        

        customer_id = deposit_form.customer_id.data
        amount = deposit_form.amount.data
        phone_number = deposit_form.phone_number.data
        transaction_time = datetime.now()
        if amount > 0:
            # create customer object
            send_money_request(amount, phone_number) # send mpesa request
            customer = Customers.query.get(customer_id)
            transaction = Transactions(amount = amount, transaction_type = TransactionType.DEBIT.name, transaction_time = transaction_time, transaction_method = TransactionMethod.MPESA.name)
            customer.bank_balance = customer.bank_balance + amount
            # add transactions as a child reference of the customer table
            customer.transactions.append(transaction)


            try:
                db.session.add(customer)
                db.session.commit()
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("Failed to add customer")
                flash('Database Error: Failed to process transaction')
                print(e)
            else:
                # on successful saving
                flash('Pending record...Awaiting MPESA Confirmation')
                # send emails
                send_admin_message(transaction_subject = "[MIFS]:Successful MPESA Deposit", transaction_message = f'An M-PESA deposit transaction of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} by {customer.user.name} was succesful')
                send_customer_message(customer.user.email, transaction_subject = "[MIFS]:Successful MPESA Deposit", transaction_message = f'Your MPESA Deposit of {amount}  at {transaction_time.strftime("%Y:-%M-%d: %H:%M")} was succesful' )
        else:
            flash("Amount has to be greater than zero")
    else:
        print("Form not validated")

    return render_template("admin/add_mpesa_deposit.html", deposit_form = deposit_form)




#-----------------------------------------------------
@admin.route('/find_mpesa_customer', methods = ["GET"])
@login_required
def find_mpesa_cutomer():
    
    customer_id = request.args.get("customer_id")
    # fetch customer by ID/ primary key
    customer = Customers.query.get(customer_id)



    if customer:
        #return balance and customer
        deposit_form = DepositForm(name = customer.user.name, balance = customer.bank_balance, phone_number = customer.mobile, customer_id = customer.id)
        
        return render_template("admin/add_mpesa_deposit.html",customer_details = customer, deposit_form = deposit_form)
    else:
        flash("No Such Customer was found")
        deposit_form = DepositForm()
        return render_template("admin/add_mpesa_deposit.html",  deposit_form = deposit_form)
        # return template pre-populated



#-------------------------------------------------------------------------
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)"""
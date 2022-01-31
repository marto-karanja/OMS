from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SubmitField,FloatField, SelectField
from wtforms.validators import InputRequired, Email
from .models import TransactionMethod

class DepositForm(FlaskForm):
    amount = FloatField('Amount to Deposit', validators=[InputRequired()])
    balance = FloatField('Current Balance')
    name = StringField('Customer Name')
    phone_number = IntegerField('Phone Number')
    description = TextAreaField('Description')
    customer_id = HiddenField('customer_id')
    submit = SubmitField('Make Deposit')

class CustomerDepositForm(FlaskForm):
    amount = FloatField('Amount to Deposit', validators=[InputRequired()])
    balance = FloatField('Current Balance')
    name = StringField('Customer Name')
    phone_number = IntegerField('Phone Number')
    description = TextAreaField('Description')
    customer_id = HiddenField('customer_id')
    submit = SubmitField('Make Deposit')

class CashDepositForm(FlaskForm):
    amount = FloatField('Amount', validators=[InputRequired()])
    payment_method = SelectField('Select Payment Method', validators=[InputRequired()], choices = [TransactionMethod.CASH.name, TransactionMethod.CREDIT_CARD.name, TransactionMethod.DEBIT_CARD.name])
    submit = SubmitField('Make Deposit')


#--------------------------------------------------------
class WithdrawForm(FlaskForm):
    """"Withdraw form"""
    amount = FloatField('Amount', validators=[InputRequired()])
    payment_method = SelectField('Select Withdrawal Method', validators=[InputRequired()], choices = [TransactionMethod.CASH.name, TransactionMethod.CREDIT_CARD.name, TransactionMethod.DEBIT_CARD.name])
    submit = SubmitField('Process Withdrawal')
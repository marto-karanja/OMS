import email
import enum

from xxlimited import Str
from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SubmitField,FloatField, SelectField, EmailField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
from .models import TransactionMethod, User



#------------------------------------------------
###Enums

class EnglishCountry(enum.Enum):
    UK = "UK English"
    US = "US English"
    AUSTRALIA = "Australia english"

class Person(enum.Enum):
    1ST = "1st Person"
    2ND = "2nd Person"
    3RD = "3rd Person"






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


########-------------------------------------------------------------
class LoginForm(FlaskForm):
    """Login form"""
    email =EmailField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember')



#######----------------------------------------------------
class RegisterForm(FlaskForm):
    name = StringField("Your Full Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email("You need to put a valid email address")])
    password = PasswordField("Password", validators =[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("confirm password", validators =[InputRequired()])
    terms = BooleanField('Terms and Services')

    def validate_email(self, field): 
        # here is where the magic is
        if User.query.filter_by(email=field.data).first(): 
            # check if in database
            raise ValidationError("This email has already been registered. Proceed to login to your account.")


#######------------------------------------------------
class OrderForm(FlaskForm):
    number_words = FloatField("Length/ number of words:", validators=[InputRequired()])
    topic = StringField("Topic:")
    description = TextAreaField("Description:")
    audience = StringField("Audience:")
    medium = StringField("Medium/Format:")
    tone = StringField("Tone:")
    person = SelectField("1st, 2nd or 3rd person?:", validators=[InputRequired()], choices = [Person.1ST.name, Person.2ND.name, Person.3RD.name])
    english_country = SelectField('English preference:', validators=[InputRequired()], choices = [EnglishCountry.UK.name, EnglishCountry.US.name, EnglishCountry.AUSTRALIA.name])
    example = StringField("Article for us to draw inspiration from:")
    research_links = TextAreaField("Research links:")
    seo = TextAreaField("SEO keywords to include:")
    description = TextAreaField("Description about your business:")
    omments = StringField("Any other comments?:")
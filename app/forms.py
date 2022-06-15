import email
from email.policy import default
import enum

from xxlimited import Str
from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SubmitField,FloatField, SelectField, EmailField, PasswordField, BooleanField, DecimalField, DateField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
from .models import Department, TransactionMethod, User, EnglishCountry, Person, Status, Department
from wtforms import MultipleFileField




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
    number_words = StringField("Length/ number of words:", validators=[InputRequired()])
    topic = StringField("Topic:")
    description = TextAreaField("Description:")
    audience = StringField("Audience:")
    medium = StringField("Medium/Format:")
    tone = StringField("Tone:")
    person = SelectField("1st, 2nd or 3rd person?:", validators=[InputRequired()], choices = [(Person.FIRST.name,Person.FIRST.value), (Person.SECOND.name,Person.SECOND.value), ( Person.THIRD.name, Person.THIRD.value)])
    english_country = SelectField('English preference:', validators=[InputRequired()], choices = [(EnglishCountry.UK.name, EnglishCountry.UK.value), (EnglishCountry.US.name, EnglishCountry.US.value),(EnglishCountry.AUSTRALIA.name, EnglishCountry.AUSTRALIA.value)])
    example = StringField("Article for us to draw inspiration from:")
    research_links = TextAreaField("Research links:")
    seo = StringField("SEO keywords to include:")
    business_description = TextAreaField("Description about your business:")
    comments = StringField("Any other comments?:")
    price = DecimalField("Price:", places=2)
    deadline_date = StringField("Due day:", validators=[InputRequired()])
    deadline_time = StringField("Due time:", validators=[InputRequired()])
    order_status = SelectField('Order Status:', validators=[InputRequired()], choices = [(Status.unassigned.name, Status.unassigned.value), (Status.bid_status.name, Status.bid_status.value)])



#####--------------------------------------------------------------------
class AssignForm(FlaskForm):
    writer_name = SelectField("Choose Writer:", coerce=int)
    bid_writers = SelectField("Writers who Bid:", coerce=str)
    order_status = SelectField('Set Order Status to:', validators=[InputRequired()], choices = [(Status.unassigned.name, Status.unassigned.value),(Status.bid_status.name, Status.bid_status.value),(Status.progress.name, Status.progress.value), (Status.revision.name, Status.revision.value),  (Status.completed.name, Status.completed.value),  (Status.finished.name, Status.finished.value),  (Status.paid.name, Status.paid.value)])



###---------------------------------------------------------------------------------------
class FileForm(FlaskForm):
    
    files = MultipleFileField('File(s) Upload', validators=[InputRequired()])
    description = StringField('Description')


####-----------------------------------------------------------------------------------
class MessageForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()])
    to_department = SelectField('Message Recipient', validators=[InputRequired()], choices = [(Department.EDITOR.name, Department.EDITOR.value),(Department.FINANCE.name, Department.FINANCE.value) , (Department.QUALITY.name, Department.QUALITY.value), (Department.CUSTOMER.name, Department.CUSTOMER.value)])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')


######--------------------------------------------------------------------
class AdminMessageForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()])
    to_department = SelectField('Message Recipient', validators=[InputRequired()], choices = [(Department.WRITER.name, Department.WRITER.value), (Department.EDITOR.name, Department.EDITOR.value),(Department.FINANCE.name, Department.FINANCE.value) , (Department.QUALITY.name, Department.QUALITY.value), (Department.CUSTOMER.name, Department.CUSTOMER.value)])
    from_department = SelectField('Department from', validators=[InputRequired()], choices = [(Department.ADMIN.name, Department.ADMIN.value), (Department.EDITOR.name, Department.EDITOR.value),(Department.FINANCE.name, Department.FINANCE.value) , (Department.QUALITY.name, Department.QUALITY.value), (Department.CUSTOMER.name, Department.CUSTOMER.value)])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')


from wtforms import Form, BooleanField


def create_dynamic_checkbox(list_a):
    class Prefs(FlaskForm):
        pass

    for ele in list_a:
        setattr(Prefs, ele, BooleanField(ele))

    return Prefs
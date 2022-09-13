import enum
import datetime

from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.schema import FetchedValue
from sqlalchemy import text
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
    EDITOR = "Editor"
    WRITER = "Writer"
    ADMIN = "Admin"


class EnglishCountry(enum.Enum):
    UK = "UK English"
    US = "US English"
    AUSTRALIA = "Australia english"

class Person(enum.Enum):
    FIRST = "1st Person"
    SECOND = "2nd Person"
    THIRD = "3rd Person"

class Status(enum.Enum):
    unassigned = "Unassigned"
    bid_status = "Bid Status"
    progress = "In Progress"
    reassigned = "Reassigned"
    completed = "Completed"
    revision = "Revision"
    finished = "Finished"
    paid = "Paid"
    disputed = "Disputed"
    cancelled = "Cancelled"

class EducationLevel(enum.Enum):
    HIGH_SCHOOL = "High School"
    UNDERGRADUATE = "Undergraduate"
    DIPLOMA = "Diploma"
    CERTIFICATE = "Certificate" 


class Order_type(enum.Enum):
    CUSTOMER = "Customer File"
    WRITER = "Writer File"
    EDITOR= "Editor File"

class Length_type(enum.Enum):
    WORDS = "Words"
    PAGES = "Pages"


"""
class TaskProgress(enum.Enum):
    Ongoing = "Ongoing"
    Completed = "Bid Status"
"""


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    number = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_type = db.Column(db.Enum(AccountType))
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # to del
    customers = db.relationship('Customers', backref='user', uselist = False, lazy=True)
    #orders = db.relationship('Orders', backref='user', secondary='user', lazy=True)
    #orders = db.relationship("Orders", foreign_keys = "Orders.writer_id", backref=db.backref('writer_assigned', lazy='dynamic'))
    orders = db.relationship("Orders", back_populates="writer", foreign_keys = '[Orders.writer_id]', lazy="select")
    edit_orders = db.relationship("Orders", back_populates="editor", foreign_keys = '[Orders.editor_id]', lazy="dynamic")
    #editor = db.relationship("Orders", foreign_keys="Orders.editor_id", backref=db.backref('editor', lazy= True))
    # to del
    transactions = db.relationship('Transactions', backref='transactions', lazy=True)
    #author = db.Column('Messages', foreign_keys='Messages.sender_id', lazy='dynamic')
    #author = db.Column(db.Integer, db.ForeignKey('messages.sender_id'))
    """
    messages_sent = db.relationship("Messages", back_populates="sender", foreign_keys='Messages.sender_id')
    #recipient = db.Column('Messages',foreign_keys='Messages.recipient_id', lazy='dynamic')
    #recipient = db.Column(db.Integer, db.ForeignKey('messages.recipient_id'))
    messages_received = db.relationship('Messages', back_populates="recipient", foreign_keys='Messages.recipient_id')"""
    
    messages_sent = db.relationship('Messages',
                                    foreign_keys='Messages.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Messages',
                                        foreign_keys='Messages.recipient_id',
                                        backref='receiver', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    payments = db.relationship("Payments", back_populates="writers", lazy='joined')
    fines = db.relationship("Fines", back_populates="writers", lazy='joined')
    ####
    profile_image_path = db.Column(db.String(1000))
    about_me = db.Column(db.Text())
    ranking = db.Column(db.String(100))
    education_level = db.Column(db.Enum(EducationLevel))
    certificate_path = db.Column(db.String(1000))
    mysql_auto_increment='1001'

    # ...

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Messages.query.filter_by(recipient=self).filter(
            Messages.timestamp > last_read_time).count()


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
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    paper_length = db.Column(db.Float())
    page_words = db.Column(db.Enum(Length_type))
    topic = db.Column(db.String(1000))
    description = db.Column(db.Text())
    audience = db.Column(db.String(1000))
    medium = db.Column(db.String(1000))
    tone = db.Column(db.String(1000))
    person = db.Column(db.Enum(Person))
    english_country = db.Column(db.Enum(EnglishCountry))
    example = db.Column(db.String(1000))
    research_links = db.Column(db.Text())
    seo = db.Column(db.String(1000))
    business_description = db.Column(db.Text())
    comments = db.Column(db.String(1000))
    rating = db.Column(db.Integer, server_default = "5")
    status = db.Column(db.Enum(Status), nullable = False,server_default=Status.unassigned.name)
    price = db.Column(db.Numeric(65,2))
    deadline = db.Column(db.DateTime())
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    editor_id = db.Column(db.Integer,  db.ForeignKey('user.id'), index=True)
    editor = db.relationship("User", back_populates="edit_orders", foreign_keys = '[Orders.editor_id]')
    
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    writer = db.relationship("User", back_populates="orders", foreign_keys = '[Orders.writer_id]')
    #writer = db.relationship("User", foreign_keys=[writer_id], backref=db.backref('writer', lazy='dynamic'))
    files = db.relationship('FileOrders', back_populates="order")
    messages = db.relationship('Messages', back_populates="order")
    

class OrderTransactions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='OrderTransactions.order_id', backref=db.backref('transaction_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='OrderTransactions.editor_id', backref=db.backref('transaction_editor', lazy='dynamic'))
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship("User", foreign_keys='OrderTransactions.writer_id', backref=db.backref('transaction_writer', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    #status = db.Column(db.Enum(TaskProgress))
    

class CurrentOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='CurrentOrders.order_id', backref=db.backref('current_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='CurrentOrders.editor_id', backref=db.backref('current_editor', lazy='dynamic'))
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship("User", foreign_keys='CurrentOrders.writer_id', backref=db.backref('current_writer', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())

class Writers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    writers_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship("User", foreign_keys='Writers.writers_id', backref=db.backref('writer_table', lazy='dynamic'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='Writers.order_id', backref=db.backref('order', lazy='dynamic'))
    job_status = db.Column(db.Enum(Status))
    rating = db.Column(db.Integer, server_default = "5")
    amount_paid = db.Column(db.Numeric(65,2), server_default = "0")
    amount_fined = db.Column(db.Numeric(65,2), server_default = "0")
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())


class BiddingOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='BiddingOrders.order_id', backref=db.backref('bidding_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='BiddingOrders.editor_id', backref=db.backref('bid_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    bids = db.relationship("Bids",  backref=db.backref('bid_order', lazy='joined'))
    #bids = db.relationship("Bids", back_populates="bid_order")

class Bids(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bidding_id = db.Column(db.Integer, db.ForeignKey(BiddingOrders.id))    
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship("User", foreign_keys='Bids.writer_id', backref=db.backref('bid_writers', lazy='joined'))
    #bid_order = db.relationship("BiddingOrders", back_populates="bids")
    

class UnassignedOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='UnassignedOrders.order_id', backref=db.backref('unassigned_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='UnassignedOrders.editor_id', backref=db.backref('unassigned_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())


class CompletedOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='CompletedOrders.order_id', backref=db.backref('completed_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='CompletedOrders.editor_id', backref=db.backref('completed_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())

class RevisionOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='RevisionOrders.order_id', backref=db.backref('revision_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='RevisionOrders.editor_id', backref=db.backref('revision_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    deadline = db.Column(db.DateTime())

class FinishedOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='FinishedOrders.order_id', backref=db.backref('finished_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='FinishedOrders.editor_id', backref=db.backref('finished_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())

class Payments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writers = db.relationship("User", back_populates = "payments", lazy="joined")
    orders = db.relationship("PaidOrders", back_populates="payment", lazy="joined")
    payment_date = db.Column(db.TIMESTAMP)
    amount_paid = db.Column(db.Numeric(65,2))
    description = db.Column(db.String(1000))

class Fines(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writers = db.relationship("User", back_populates = "fines", lazy="joined")
    orders = db.relationship("FineOrders", back_populates="fine", lazy="joined")
    fine_date = db.Column(db.TIMESTAMP)
    amount_fined = db.Column(db.Numeric(65,2))
    description = db.Column(db.String(1000))

class FineOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='FineOrders.order_id', backref=db.backref('fine_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='PaidOrders.editor_id', backref=db.backref('paid_editor', lazy='dynamic'))
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='FineOrders.editor_id', backref=db.backref('fine_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    fine_id = db.Column(db.Integer, db.ForeignKey(Fines.id))
    fine = db.relationship("Fines", back_populates="orders")




class PaidOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", foreign_keys='PaidOrders.order_id', backref=db.backref('paid_order', lazy='dynamic'))
    description = db.Column(db.Text())
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='PaidOrders.editor_id', backref=db.backref('paid_editor', lazy='dynamic'))
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='PaidOrders.editor_id', backref=db.backref('paid_editor', lazy='dynamic'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    payment_id = db.Column(db.Integer, db.ForeignKey(Payments.id))
    payment = db.relationship("Payments", back_populates="orders")


    




##---------------------------------------------------

class Department(enum.Enum):
    EDITOR = "Editor's Department"
    FINANCE = "Finance Department"
    QUALITY = "Quality Department"
    CUSTOMER = "Customer"
    WRITER = "Writer's message"
    ADMIN = "Admin Department"

#---------------------------------------------------

class ThreadStatus(enum.Enum):
    PARENT = "Parent thread"
    CHILD = "Child thread"
    DELETED = "Deleted"

class ReadStatus(enum.Enum):
    TRUE = "True"
    FALSE = "False"







#-------------------------

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, index=True,)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True,)
    sender = db.relationship("User", back_populates="messages_sent", foreign_keys='Messages.sender_id')
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True,)
    order = db.relationship("Orders", back_populates="messages")
    #department = db.Column(db.Enum(Department)) # to be deleted
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True,)
    recipient = db.relationship("User", back_populates="messages_received", foreign_keys='Messages.recipient_id')

    subject = db.Column(db.String(1000))
    message = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, server_default=func.now())
    sent_to = db.Column(db.Enum(Department), index=True,)
    sent_from = db.Column(db.Enum(Department), index=True,)
    thread_status = db.Column(db.Enum(ThreadStatus),server_default=ThreadStatus.CHILD.name)
    read_status = db.Column(db.Enum(ReadStatus),server_default=ReadStatus.FALSE.name)







#---------------------------------------------------------------------------------
class FileOrders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", back_populates="files")
    file_location = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    type = db.Column(db.Enum(Order_type))
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship("User", foreign_keys='FileOrders.writer_id', backref=db.backref('file_writer'))
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship("User", foreign_keys='FileOrders.editor_id', backref=db.backref('file_editor'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_edited = db.Column(db.TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())




#--------------------------------------------------------------------------------------



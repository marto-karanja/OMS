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





from app.models import BiddingOrders, CompletedOrders, CurrentOrders, EducationLevel, FileOrders, OrderTransactions, Orders, User, Customers, Transactions, TransactionType, TransactionMethod, AccountType, EnglishCountry, Person, Status, Orders, Bids, Order_type, Messages, Department, ThreadStatus, ReadStatus
from app import db
from app.emails import send_message, send_admin_message, send_customer_message
from app.forms import AssignForm, DepositForm, LoginForm, OrderForm, AssignForm, FileForm, MessageForm, ReplyMessageForm, ReplyThreadedMessageForm, WriterOrderReplyMessageForm, UserEditForm
from app.app.admin.admin_views import find_time_difference


from flask_sqlalchemy import SQLAlchemy

writer = Blueprint('writer', __name__)


@writer.route('/writers_dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    orders = Orders.query.filter(Orders.writer_id == session['user_id']).all()
    for order in orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("writer/writer_dashboard.html", orders = orders)
    

##_---------------------------------------------------------------------------
@writer.route('/view_order?<order_id>', methods = ["GET", "POST"])
@login_required
def view_order(order_id):
    order = Orders.query.options(joinedload("files")).get(order_id)
    # check if order is in bid status or take(unsassigned) status
    # if bid check if writer has bid for the order
    # else if unassigned, display take button
    if order.status == Status.bid_status:
        bid_order = BiddingOrders.query.filter(BiddingOrders.order == order).first()

        order.bid_status = False
        bid_writers = [ g.writer_id for g in bid_order.bids]
        print(bid_writers)
        if session['user_id'] in bid_writers:
            order.bid_status = True

    messages = Messages.query.filter((Messages.thread_status == ThreadStatus.PARENT) & (Messages.order_id == order.id)).all()

    file_form = FileForm()
    message_form = MessageForm()

    return render_template("writer/view_order.html", Status = Status, order= order, file_form = file_form, message_form = message_form, messages = messages)




#-----------------------------------------------------------------------------------------
@writer.route('/view_available_orders', methods = ["GET", "POST"])
@login_required
def view_available_orders():
    orders = Orders.query.filter((Orders.status == Status.unassigned) | (Orders.status == Status.bid_status)).all()
    for order in orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("writer/writer_dashboard.html", orders = orders)





#-----------------------------------------------------------------------------------------
@writer.route('/view_progress_orders', methods = ["GET", "POST"])
@login_required
def progress_orders():
    orders = Orders.query.filter((Orders.status == Status.unassigned) | (Orders.status == Status.bid_status)).all()
    for order in orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("writer/writer_dashboard.html", orders = orders)


#-----------------------------------------------------------------------------------------
@writer.route('/view_revision_orders', methods = ["GET", "POST"])
@login_required
def revision_orders():
    orders = Orders.query.filter((Orders.status == Status.revision) & (Orders.writer_id == session["user_id"])).all()
    for order in orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("writer/writer_dashboard.html", orders = orders)





#-----------------------------------------------------------------------------------------
@writer.route('/view_bid_orders', methods = ["GET", "POST"])
@login_required
def bid_orders():
    bid_orders = []
    orders = Orders.query.filter(Orders.status == Status.bid_status).all()
    for order in orders:
        bid = BiddingOrders.query.filter(BiddingOrders.order_id == order.id).first()
        
        if session['user_id'] in [g.writer_id for g in bid.bids]:
            bid_orders.append(order)

    for order in bid_orders:        
        order.difference = find_time_difference(order.deadline)
    return render_template("writer/writer_dashboard.html", orders = bid_orders)




##_---------------------------------------------------------------------------
@writer.route('/bid_order?<order_id>', methods = ["GET", "POST"])
@login_required
def bid_order(order_id):
    bidding_order = BiddingOrders.query.filter_by(order_id = order_id).first()
    #### Set bid status
    bid = Bids(
        writer_id = session['user_id'],
        bidding_id = bidding_order.id

    )
    transanction = OrderTransactions(
        order_id= order_id,
        description = "Bid for order {} placed by a writer ".format(order_id,session['name']),
        writer_id = session['user_id']

    )
    
    
    try:
        db.session.add(bid)
        db.session.add(bidding_order)
        db.session.add(transanction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to place bid")
        flash('Database Error: Failed to place bid')
        print(e)
    else:
        # on successful saving
        flash('Bid for {} was placed successfully. You will receive a notification in case you are assigned.'.format(bidding_order.order.id))
        return redirect(url_for("writer.view_order", order_id= bidding_order.order.id))




    return redirect(url_for("writer.view_order", order_id= bidding_order.order.id))


##_---------------------------------------------------------------------------
@writer.route('/take_order?<order_id>', methods = ["GET", "POST"])
@login_required
def take_order(order_id):
    order = Orders.query.get(order_id)

    order.writer_id = session['user_id']
    order.status = Status.progress

    # create current order entry
    current = CurrentOrders(
        order_id = order_id,
        description = "Order taken by [{}]".format(session['name']),
        writer_id = session['user_id']
    )
   

    # create transaction entry
    transanction = OrderTransactions(
        order_id= order_id,
        description = "Bid for order {} placed by a writer ".format(order_id,session['name']),
        writer_id = session['user_id']

    )
    
    try:
        db.session.add(order)
        db.session.add(current)
        db.session.add(transanction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to place bid")
        flash('Database Error: Failed to place bid')
        print(e)
    else:
        # on successful saving
        flash('You were assigned this order successfully. You can start working on the order')
        return redirect(url_for("writer.view_order", order_id= order.id))



##_---------------------------------------------------------------------------
@writer.route('/complete_order?<order_id>', methods = ["GET", "POST"])
@login_required
def complete_order(order_id):
    order = Orders.query.get(order_id)

    order.writer_id = session['user_id']
    order.status = Status.completed

    # create current order entry
    complete = CompletedOrders(
        order_id = order_id,
        description = "Order taken by [{}]".format(session['name']),
        #writer_id = session['user_id']
    )
   

    # create transaction entry
    transanction = OrderTransactions(
        order_id= order_id,
        description = "Bid for order {} placed by a writer ".format(order_id,session['name']),
        writer_id = session['user_id']

    )
    
    try:
        db.session.add(order)
        db.session.add(complete)
        db.session.add(transanction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to place bid")
        flash('Database Error: Failed to place bid')
        print(e)
    else:
        # on successful saving
        flash('You have successfully completed this order.')
        return redirect(url_for("writer.view_order", order_id= order.id))

    


    return redirect(url_for("writer.view_order", order_id= order.id))
    

##_---------------------------------------------------------------------------
@writer.route('/upload_file?<order_id>', methods = ["GET", "POST"])
@login_required
def upload_order_file(order_id):
    order = Orders.query.options(joinedload("files")).get(order_id)
    file_form = FileForm()

    if file_form.validate_on_submit():
        # get file data

        files = file_form.files.data
        saved_files = []
        basedir = os.path.abspath(os.path.dirname(__file__))
        for file in files:
            file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], file.filename))

            loc = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)

            # save file data
            ## create file object
            file = FileOrders(
                order = order,
                type = Order_type.WRITER,
                description = file_form.description.data,                
                file_location = loc,
                writer_id = session['user_id']
            )
            saved_files.append(file)

        try:
            for f in saved_files:
                db.session.add(f)
            db.session.commit()
        except Exception as e:
            # for resetting non-commited .add()
            db.session.rollback()
            db.session.flush()
            flash('Failed to upload orders successfullu')
            print(e)
        else:
            # on successful saving
            flash("File was uploaded successfully")
        return redirect(url_for("writer.view_order", order_id = order.id, _anchor='files'))

    return redirect(url_for("writer.view_order", order_id = order.id))


##_---------------------------------------------------------------------------
@writer.route('/send_message?<order_id>', methods = ["GET", "POST"])
@login_required
def send_message(order_id):
    # get message
    
    # get recipient
    # save to database]
    
    # add file upload mechanism

    message_form = MessageForm()
    if message_form.validate_on_submit():
        

        message =  Messages(
            sender_id = session['user_id'],
            subject = message_form.subject.data,
            order_id = order_id,
            message = message_form.message.data,
            sent_to = message_form.to_department.data,
            sent_from = Department.WRITER.value,
            thread_status = ThreadStatus.PARENT
        )
        
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Message was not sent')
            print(e)
        else:
            # on successful saving
            flash("Message was sent successully")
    return redirect(url_for("writer.view_order", order_id = order_id, _anchor='files'))


#####---------------------------------------------------------------------------------------

@writer.route('/static/upload/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)

@writer.route('/writer_view_inbox')
@login_required
def writer_view_inbox():
    page = request.args.get('page', 1, type=int)

    messages = Messages.query.filter((Messages.recipient_id == session['user_id']) & (Messages.thread_status == ThreadStatus.PARENT)).order_by(Messages.id.desc()).paginate(page, 10, False)
    
    message_form = MessageForm()

    return render_template("writer/messages.html", messages = messages.items, message_form = message_form )



#---------------------------------------------------------------------
@writer.route('/writer_view_unread')
@login_required
def writer_view_unread():

    page = request.args.get('page', 1, type=int)

    messages = Messages.query.filter((Messages.recipient_id == session['user_id']) & (Messages.thread_status == ThreadStatus.PARENT) & (Messages.read_status == ReadStatus.FALSE)).order_by(Messages.id.desc()).paginate(page, 10, False)

    message_form = MessageForm()
    return render_template("writer/messages.html", messages = messages.items, message_form = message_form)



####--------------------------------------------------------------------------------- 

@writer.route('/writer_view_outbox')
@login_required
def writer_view_outbox():

    page = request.args.get('page', 1, type=int)

    messages = Messages.query.filter((Messages.sender_id == session['user_id']) & (Messages.thread_status == ThreadStatus.PARENT)).order_by(Messages.id.desc()).paginate(page, 10, False)

    message_form = MessageForm()
    return render_template("writer/outbox.html", messages = messages.items, message_form = message_form)



###--------------------------------------------------------------------------------------


@writer.route('/unpaid_orders')
@login_required
def unpaid_orders():
    orders = Orders.query.filter((Orders.status == Status.completed) & (Orders.writer_id == session['user_id'])).all()
    return render_template("writer/unpaid_orders.html", orders = orders)



#--------------------------------------------------------------------


#-view message detail
####-------------------------------------------------------------------------
@writer.route('/writer_view_message?<message_id>', methods = ['GET', 'POST'])
@login_required
def view_message_detail(message_id):
    """Renders view for a single message"""
    # fetch customer by ID/ primary key
    message = Messages.query.options(joinedload(Messages.order)).get(message_id)
    order = message.order


    order.time_remaining = find_time_difference(order.deadline)

    file_form = FileForm()
    message_form = WriterOrderReplyMessageForm(order_id = order.id, thread_id = message.id)
    
    messages = Messages.query.filter(Messages.thread_id == message_id).order_by(desc(Messages.timestamp)).all()

    return render_template("writer/order_message_single.html", Status = Status, order= order, file_form = file_form, message_form = message_form, detailed_message = message, messages = messages)



#-reply to order message
####-------------------------------------------------------------------------
@writer.route('/writer_reply_order_message', methods = ['POST'])
@login_required
def reply_order_message():
    message_form = WriterOrderReplyMessageForm()
    if message_form.validate_on_submit():
        parent_message = Messages.query.get(message_form.thread_id.data)
        
        

        
        message =  Messages(
            sender_id = session['user_id'],
            #recipient_id = order.writer_id,
            thread_id = message_form.thread_id.data,
            subject = parent_message.subject,
            order_id = message_form.order_id.data,
            message = message_form.message.data,
            sent_to = parent_message.sent_to,
            sent_from = parent_message.sent_from,
            thread_status = ThreadStatus.CHILD
        )
        
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Message was not sent')
            print(e)
        else:
            # on successful saving
            flash("Message was sent successully")
    else:
        print("Form not validated")
        flash("Form was not validated successfully")
    return redirect(url_for("writer.view_order_messages", order_id = message_form.order_id.data, _anchor='files'))

#-View order messages
####-------------------------------------------------------------------------
@writer.route('/writer_view_order_messages?<order_id>', methods = ['GET','POST'])
@login_required
def view_order_messages(order_id):
    order = Orders.query.options(joinedload("files")).get(order_id)

    if order.status == Status.bid_status:
        bid_order = BiddingOrders.query.filter(BiddingOrders.order == order).first()

        order.bid_status = False
        bid_writers = [ g.writer_id for g in bid_order.bids]
        print(bid_writers)
        if session['user_id'] in bid_writers:
            order.bid_status = True

    messages = Messages.query.filter((Messages.thread_status == ThreadStatus.PARENT) and (Messages.order_id == order_id)).all()

    file_form = FileForm()
    message_form = MessageForm()

    return render_template("writer/view_order_messages.html", Status = Status, order= order, file_form = file_form, message_form = message_form, messages = messages)

#-Return compose message form
####-------------------------------------------------------------------------
@writer.route('/writer_compose_message', methods = ['GET','POST'])
@login_required
def compose_message():
    """Create new message"""
    message_form = MessageForm()
    return render_template("writer/email_compose.html", message_form = message_form)


#-Create order messages
####-------------------------------------------------------------------------
@writer.route('/writer_send_message', methods = ['GET','POST'])
@login_required
def compose_writer_message():
    message_form = MessageForm()
    if message_form.validate_on_submit():
        
        message =  Messages(
            sender_id = session['user_id'],
            subject = message_form.subject.data,
            sent_to = message_form.to_department.data,
            message = message_form.message.data,
            sent_from = Department.WRITER,
            thread_status = ThreadStatus.PARENT
        )
        
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Message was not sent')
            print(e)
        else:
            # on successful saving
            
            flash("Message was sent successully")
            return redirect(url_for('writer.compose_message'))
    else:
        print("Form not validated")
        flash("Form was not validated successfully")
    return render_template("writer/email_compose.html", message_form = message_form )



#-View message details
####-------------------------------------------------------------------------
@writer.route('/inbox_message_detail?<message_id>', methods = ['GET','POST'])
@login_required
def inbox_message_detail(message_id):
    page = request.args.get('page', 1, type=int)

    threaded_messages = Messages.query.filter((Messages.thread_id == message_id)).order_by(desc(Messages.timestamp)).paginate(page, 10, False)
    message = Messages.query.get(message_id)

    # update read field
    message.read_status = ReadStatus.TRUE
    db.session.add(message)
    db.session.commit()

    message_form = ReplyThreadedMessageForm()
    create_message_form = MessageForm()

    return render_template("writer/message_detail.html", message = message, threaded_messages = threaded_messages.items, message_form = message_form, create_message_form = create_message_form)


###--------------------------------------------------------------------------------------


@writer.route('/user_profile')
@login_required
def user_profile():
    user_profile = User.query.get(session["user_id"])

    form = UserEditForm()
    form.phone_number.data = user_profile.number
    form.about_me.data = user_profile.about_me or "Enter a short description about yourself"
    form.education_level.data = user_profile.education_level or EducationLevel.UNDERGRADUATE.name
    
    return render_template("writer/user-profile.html", user_profile = user_profile, form = form)


###--------------------------------------------------------------------------------------


@writer.route('/update_writer_profile', methods = ['GET','POST'])
@login_required
def update_writer_profile():
    user_profile = User.query.get(session["user_id"])
    form = UserEditForm()
    if form.validate_on_submit():
        user_profile.number = form.phone_number.data
        user_profile.about_me = form.about_me.data
        user_profile.education_level = form.education_level.data
        # save session
        try:
            print("hapa")
            db.session.add(user_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Profile was not updated successfully')
            print(e)
        else:
            # on successful saving
            
            flash("Profile was updated successfully")
            
    else:
        flash('Error: Profile was not updated successfully')
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)

    
    # update database profile
    # save profile picture
    # save certificate path
    return redirect(url_for("writer.user_profile"))


#----------------------------------------------------------------------------
@writer.route('/edit_user_profile')
@login_required
def edit_user_profile():
    user_profile = User.query.get(session["user_id"])

    form = UserEditForm()
    form.phone_number.data = user_profile.number
    form.about_me.data = user_profile.about_me or "Enter a short description about yourself"
    form.education_level.data = user_profile.education_level or EducationLevel.UNDERGRADUATE.name
    
    return render_template("writer/user-edit-profile.html", user_profile = user_profile, form = form)

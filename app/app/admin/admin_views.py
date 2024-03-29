import logging
from bisect import bisect
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
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy import desc, asc
from flask import current_app
from flask import Markup
from dateutil.parser import parse
from werkzeug.security import generate_password_hash
from flask import send_from_directory



from app.models import BiddingOrders, Bids, CurrentOrders, FileOrders, OrderTransactions, Orders, User, Customers, Transactions, TransactionType, TransactionMethod, AccountType, EnglishCountry, Person, Status, Order_type, Messages, Department, Writers, Payments, ThreadStatus
from app import db, app
from app.emails import send_message, send_admin_message, send_customer_message
from app.forms import AssignForm, DepositForm, LoginForm, OrderForm, AssignForm, FileForm, MessageForm, AdminMessageForm, ReassignForm, create_dynamic_checkbox, ReplyMessageForm, ReassignForm, CompleteForm, RevisionForm
from app.mpesa import send_money_request
from app.scripts.scripts import set_bidding_status, set_order_progress, set_order_unassigned, Actions, Operations, set_orders_as_paid, set_order_rating

from flask_sqlalchemy import SQLAlchemy


admin = Blueprint('admin', __name__)

logger = logging.getLogger('Admin View')

#------------------------------------------------------------


# --------------------------------------------------


#-------------------------------------------------------------------------

@admin.route('/', methods=["GET", "POST"])
def home():
    form = LoginForm()

    return render_template("pages/writergigs_login.html", login_form = form)

#-------------------------------------------------------------------------------------
@admin.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status != Status.deleted).order_by(asc(Orders.deadline)).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)
        
    prev_url, next_url = return_page_links(orders, 'admin.dashboard')

    return render_template("admin/editor/editor_dashboard.html", orders = orders.items, next_url = next_url, prev_url = prev_url)



def return_page_links(items, destination_string):
    next_url = url_for(destination_string,  page=items.next_num) \
        if items.has_next else None
    prev_url = url_for(destination_string, page=items.prev_num) \
        if items.has_prev else None

    return prev_url, next_url



##---return all orders
#-------------------------------------------------------------------------
@admin.route('/all_orders', methods=["GET", "POST"])
@login_required
def all_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status != Status.deleted).order_by(asc(Orders.deadline)).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.all_orders')



    return render_template("admin/editor/all_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)



##---return orders in progress
#-------------------------------------------------------------------------
@admin.route('/progress_orders', methods=["GET", "POST"])
@login_required
def progress_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.progress).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.progress_orders')

    return render_template("admin/editor/progress_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)



##---return orders under bidding
#-------------------------------------------------------------------------
@admin.route('/bid_orders', methods=["GET", "POST"])
@login_required
def bid_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.bid_status).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.bid_orders')

    return render_template("admin/editor/bid_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


##---return orders under revision status
#-------------------------------------------------------------------------
@admin.route('/revision_orders', methods=["GET", "POST"])
@login_required
def revision_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.revision).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.revision_orders')

    return render_template("admin/editor/revision_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


##---return orders under disputed status
#-------------------------------------------------------------------------
@admin.route('/disputed_orders', methods=["GET", "POST"])
@login_required
def disputed_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.disputed).paginate(page, current_app.config['POSTS_PER_PAGE'], False)


    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.disputed_orders')

    return render_template("admin/editor/disputed_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)



##---return orders under cancelled status
#-------------------------------------------------------------------------
@admin.route('/cancelled_orders', methods=["GET", "POST"])
@login_required
def cancelled_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.cancelled).paginate(page, current_app.config['POSTS_PER_PAGE'], False)


    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.cancelled_orders')

    return render_template("admin/editor/cancelled_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


##---return orders under completed status
#-------------------------------------------------------------------------
@admin.route('/completed_orders', methods=["GET", "POST"])
@login_required
def completed_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.completed).paginate(page, current_app.config['POSTS_PER_PAGE'], False)


    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)
    
    prev_url, next_url = return_page_links(orders, 'admin.completed_orders')

    return render_template("admin/editor/completed_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)

#---return orders under completed status
#-------------------------------------------------------------------------
@admin.route('/finished_orders', methods=["GET", "POST"])
@login_required
def finished_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.finished).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.finished_orders')

    return render_template("admin/editor/finished_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


##---return orders under disputed status
#-------------------------------------------------------------------------
@admin.route('/paid_orders', methods=["GET", "POST"])
@login_required
def paid_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.paid).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.paid_orders')

    return render_template("admin/editor/paid_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


##---return orders under disputed status
#-------------------------------------------------------------------------
@admin.route('/deleted_orders', methods=["GET", "POST"])
@login_required
def deleted_orders():
    page = request.args.get('page', 1, type=int)
    orders = Orders.query.filter(Orders.status == Status.deleted).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    for order in orders.items:        
        order.difference = find_time_difference(order.deadline)

    prev_url, next_url = return_page_links(orders, 'admin.paid_orders')

    return render_template("admin/editor/deleted_orders.html", orders = orders.items, next_url = next_url, prev_url = prev_url)


@admin.route('/edit_order_details?<order_id>', methods = ["GET", "POST"])
@login_required
def edit_order_details(order_id):
    order = Orders.query.get(order_id)
    form = OrderForm()

    form.number_words.data = order.paper_length
    form.length_type.data = order.page_words
    form.topic.data = order.topic
    form.description.data = order.description
    form.audience.data = order.audience
    form.medium.data = order.medium
    form.tone.data = order.tone
    form.person.data = order.person
    form.english_country.data = order.english_country
    form.example.data = order.example
    form.research_links.data = order.research_links 
    form.seo.data = order.seo
    form.business_description.data = order.business_description
    form.comments.data = order.comments 
    form.price.data = order.price
    form.customer_price.data = order.customer_price
    form.deadline_date.data = order.deadline.strftime('%Y-%m-%d %H:%M:%S').split()[0]
    form.deadline_time.data = order.deadline.strftime('%Y-%m-%d %H:%M:%S').split()[1] 
            
    
    return render_template("admin/editor/update_order.html", order_form = form, order_id = order_id)



#------------------------------------------------------------------------
def find_time_difference(deadline):
    """Helper method to find format time difference in order"""
    current_time = datetime.datetime.now()
    try:
        difference = deadline - current_time
        time_difference = ("{} days {} Hrs {} Min".format(difference.days, difference.seconds//3600, ((difference.seconds//60) % 60)))
    except:
        time_difference = "null"
    return time_difference


""
####---------------------------------------------------------------------------------
@admin.route('/edit_order?<order_id>', methods = ["GET", "POST"])
@login_required

def edit_order(order_id):

    return prepare_order_views(order_id, template_string = "admin/editor/edit_order.html")


####---------------------------------------------------------------------------------
@admin.route('/process_order?<variable>', methods = ["POST"])
@login_required
def process_order(variable):
    # fetch customer by ID/ primary key
    order = Orders.query.get(variable)
    

    form = AssignForm()
    
    if order.status == Status.bid_status:
        form.bid_writers.choices = populate_bidding_form(order.id)
    else:
        form.bid_writers.choices = [('None','None')]
    form.writer_name.choices = [(g.id, g.name) for g in User.query.filter((User.user_type == AccountType.WRITER)).all()] 


    
    if form.validate_on_submit():
        if form.bid_writers.data == "None":
            writer_id = form.writer_name.data
            writer_name = dict(form.writer_name.choices).get(form.writer_name.data)
        else:
            writer_id = form.bid_writers.data
            writer_name = dict(form.bid_writers.choices).get(int(writer_id))
            print(form.bid_writers.choices)
            print(writer_name)
        action = form.order_status.data

        # call appropriarte function
        
        Actions[action](order, action, writer_id, writer_name)
    """
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(fieldName,err)
    """
    return redirect(url_for('admin.edit_order', order_id= order.id))

###----------------------------------------------------------------------------------

@admin.route('/set_order_revision?<order_id>', methods = ["POST", "GET"])
def set_order_revision(order_id):
    return prepare_order_views(order_id, template_string = "admin/editor/edit_revision_order.html")


###----------------------------------------------------------------------------------

@admin.route('/reassign_current_order?<order_id>', methods = ["POST", "GET"])
def reassign_current_order(order_id):
    order = Orders.query.get(order_id)
    form = ReassignForm()
    if form.validate_on_submit():
        # check if fine has been applied
        if form.fine.data:
            fine = form.fine.data
            message = f"You have been reassigned from this order. Kindly stop working on it. You have also been fined KES {fine}/ which will show in your payment profile."
        else:
            fine = 0
            message =  f"You have been reassigned from this order. Kindly stop working on it immediately."
        
            # update
            # Use message templates 

        order_payment_amount = form.payment.data
        writer_id = order.writer_id
        if order_payment_amount > 0:
            Actions["paid"](order, "paid", writer_id, order.writer.name, amount = order_payment_amount)
        if fine > 0:
            Actions["fine"](order, "reassigned", writer_id, order.writer.name, amount = order_payment_amount)

        Actions["reassigned"](order, "reassigned", writer_id, order.writer.name)







        message =  Messages(
            sender_id = session['user_id'],
            recipient_id = writer_id,
            subject = "Order Reassigned",
            order_id = order_id,
            message = message,
            sent_to = Department.WRITER.value,
            sent_from = Department.EDITOR.value,
            thread_status = ThreadStatus.PARENT
        )
            # update payments table
            # update fines table
            #set order on reassign

        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Revision Message was not sent')
            print(e)
        else:
            # on successful saving
            
            flash("Reassign Message was sent to writer successully")
            
    else:
        print("Form not validated")
        flash("Form was not validated successfully")

    return redirect(url_for("admin.set_order_revision", order_id = order_id))



####---------------------------------------------------------------------------------
@admin.route('/delete_order?<order_id>', methods = ["GET", "POST"])
@login_required

def delete_order(order_id):
    order = Orders.query.get(order_id)

    # set status to deleted
    order.status = Status.deleted

    # save database objects
    if save_db_objects(order):
        msg = "Order #{} has been moved to trash folder".format(order.id)
        flash(msg)
        logger.info(msg)
        return redirect(url_for('admin.deleted_orders'))
    else:
        msg = "Operation to delete order has been unsuccessful"
        flash(msg)
        logger.error(msg)
        return redirect(url_for('admin.edit_order', order_id= order.id))
    

def save_db_objects(obj):
    try:
        if isinstance(obj, list):
            for obj in obj:
                db.session.add(obj)
        else:
            db.session.add(obj)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        logger.exception("Operation was unsuccessful")
        return False
    else:
        # on successful saving
        logger.info("Objects saved to database successfully")
        
        return True



###----------------------------------------------------------------------------------

@admin.route('/set_order_finished?<order_id>', methods = ["POST", "GET"])
def set_order_finished(order_id):
    order = Orders.query.get(order_id)
    Actions["finished"](order, "finished", order.writer_id, order.writer.name)
    return redirect(url_for("admin.edit_order", order_id = order_id))


###----------------------------------------------------------------------------------

@admin.route('/set_order_reassigned?<order_id>', methods = ["POST", "GET"])
def set_order_reassigned(order_id):
    order = Orders.query.get(order_id)
    Actions["reassigned"](order, "reassigned", order.writer_id, order.writer.name)
    return redirect(url_for("admin.edit_order", order_id = order_id))


###----------------------------------------------------------------------------------

@admin.route('/finish_current_order?<order_id>', methods = ["POST", "GET"])
def finish_current_order(order_id):
    order = Orders.query.get(order_id)
    form = CompleteForm()
    if form.validate_on_submit():
        payment = form.payment.data
        rating = form.rating.data

        Actions["finished"](order, "finished", order.writer_id, order.writer.name, amount = payment)
        set_order_rating(writer_id = order.writer_id, order_id = order_id, rating = rating)

    return redirect(url_for("admin.edit_order", order_id = order_id))

###----------------------------------------------------------------------------------

@admin.route('/process_order_revision?<order_id>', methods = ["POST", "GET"])
def process_revision_order(order_id):
    order = Orders.query.get(order_id)
    form = RevisionForm()
    if form.validate_on_submit():
        message =  Messages(
            sender_id = session['user_id'],
            recipient_id = order.writer_id,
            subject = form.subject.data,
            order_id = order_id,
            message = form.message.data,
            sent_to = Department.WRITER.value,
            sent_from = Department.EDITOR.value,
            thread_status = ThreadStatus.PARENT
        )

        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            flash('Error: Revision Message was not sent')
            print(e)
        else:
            # on successful saving
            
            flash("Message was sent successully")
            Actions["revision"](order, "revision", order.writer_id, order.writer.name)
    else:
        print("Form not validated")
        flash("Form was not validated successfully")

    return redirect(url_for("admin.edit_order", order_id = order_id))
        
        



####------------------------------------------------------------------
@admin.route('/upload_files?<order_id>', methods = ["GET", "POST"])
@login_required
def upload_order_files(order_id):
    #
    order = Orders.query.options(joinedload("files")).get(order_id)
    file_form = FileForm()

    if file_form.validate_on_submit():
        # get file data

        files = file_form.files.data
        saved_files = []
        basedir = os.path.abspath(os.path.dirname(current_app.instance_path))
        for file in files:
            file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], file.filename))

            loc = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)

            # save file data
            ## create file object
            file = FileOrders(
                order = order,
                type = Order_type.EDITOR,
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
        return redirect(url_for("admin.edit_order", order_id = order.id))

    return redirect(url_for("admin.edit_order", order_id = order.id))    

##_---------------------------------------------------------------------------
@admin.route('/view_order_messages?<order_id>', methods = ["GET", "POST"])
@login_required
def view_order_messages(order_id):
    return prepare_order_views(order_id, template_string = "admin/editor/view_order_messages.html" )

def prepare_order_views(order_id, template_string = None):
    # fetch customer by ID/ primary key
    order = Orders.query.get(order_id)
    messages = Messages.query.filter((Messages.thread_status == ThreadStatus.PARENT) and (Messages.order_id == order_id)).all()

    form = AssignForm()
    if order.status == Status.bid_status:
        form.bid_writers.choices = populate_bidding_form(order.id)
    else:
        form.bid_writers.choices = [('None','None')]
    form.writer_name.choices = [(g.id, g.name) for g in User.query.filter((User.user_type == AccountType.WRITER)).all()]  

    order.time_remaining = find_time_difference(order.deadline)

    file_form = FileForm()
    message_form = AdminMessageForm()
    reassign_form = ReassignForm()
    complete_form = CompleteForm()
    revision_form = RevisionForm()

    if template_string == "admin/editor/edit_revision_order.html":
        return render_template(template_string, order= order, assign_form = form, messages =  messages, file_form = file_form, Status = Status, reassign_form = reassign_form, complete_form = complete_form, revision_form = revision_form)
    else:
        return render_template(template_string, order= order, assign_form = form, messages =  messages, file_form = file_form, message_form = message_form, Status = Status, reassign_form = reassign_form, complete_form = complete_form)




# Return unpaid orders
###-----------------------------------------
@admin.route('/view_unpaid_orders', methods = ["GET", "POST"])
@login_required
def unpaid_orders():
    #orders = Orders.query.filter((Orders.status == Status.completed) | (Orders.status == Status.finished)).all()
    writers = Writers.query.join(Orders, Writers.order_id == Orders.id).filter((Writers.job_status == Status.finished) | (Writers.job_status == Status.completed)).all()

    orders = [writer.order for writer in writers]

    # create checkboxes
    input_list = [str(order.id) for order in orders ]  # generate it as needed
    prefs = create_dynamic_checkbox(input_list)
    form = prefs(request.form)
    if form.validate_on_submit():
        
        writer_ids = [field.name for field in form if field.data is True]
        # store id in paid table
        # for each writer fetch completed jobs
        # save in paid tables
        # update order status


        return redirect(url_for('admin.unpaid_orders'))

    return render_template("admin/editor/unpaid_orders.html", orders = orders, form = form, zip=zip)




# return completed orders by a writer
###-------------------------------------------------------------------
@admin.route('/writer_unpaid_orders?<writer_id>', methods = ["GET", "poST"])
@login_required
def writer_unpaid_orders(writer_id):
    #orders = Orders.query.filter((Orders.status == Status.completed) & (Orders.writer_id == writer_id)).all()
    #writers = Writers.query.options(joinedload(Writers.order)).filter((Writers.job_status == Status.completed) & (Writers.writers_id == writer_id)).all()
    writers = Writers.query.join(Orders, Writers.order_id == Orders.id).filter((Writers.job_status == Status.finished) | (Writers.job_status == Status.completed) & (Writers.writers_id == writer_id)).all()

    orders = [writer.order for writer in writers]
    

    # create checkboxes
    input_list = [str(writer.order.id) for writer in writers ]  # generate it as needed
    prefs = create_dynamic_checkbox(input_list)
    form = prefs(request.form)
    if form.validate_on_submit():
        
        writer_ids = [field.name for field in form if field.data is True]
        # store id in paid table
        # for each writer fetch completed jobs
        # save in paid tables
        # update order status


        return redirect(url_for('admin.unpaid_orders'))

    return render_template("admin/editor/writer_unpaid_orders.html", writers = writers, orders= orders, form = form, zip=zip)




# return aid orders by a writer
###-------------------------------------------------------------------
@admin.route('/writer_paid_orders?<writer_id>', methods = ["GET", "poST"])
@login_required
def writer_paid_orders(writer_id):
    orders = Orders.query.filter((Orders.status == Status.paid) & (Orders.writer_id == writer_id)).all()

    # create checkboxes
    input_list = [str(order.id) for order in orders ]  # generate it as needed
    prefs = create_dynamic_checkbox(input_list)
    form = prefs(request.form)
    if form.validate_on_submit():
        
        writer_ids = [field.name for field in form if field.data is True]
        # store id in paid table
        # for each writer fetch completed jobs
        # save in paid tables
        # update order status


        return redirect(url_for('admin.unpaid_orders'))

    return render_template("admin/editor/writer_paid_orders.html", orders = orders, form = form, zip=zip)






# Return unpaid writers
###--------------------------------------------------------------
@admin.route('/view_unpaid_writers', methods = ["GET", "POST"])
@login_required
def unpaid_writers():
    """
    writers = User.query.filter(User.user_type == AccountType.WRITER)\
        .join(Orders)\
        .add_columns(db.func.sum(Orders.price).label('Order_total'))\
        .filter(User.id == Orders.writer_id)\
        .all()"""

    writers = User.query.join(Orders,  User.orders ).options(contains_eager(User.orders)).filter((Orders.status == Status.completed) | (Orders.status == Status.finished) & (User.user_type == AccountType.WRITER)).all()

    #writers = User.query.filter(User.orders.any((Orders.status == Status.completed) & (User.user_type == AccountType.WRITER))).all()


    # create checkboxes
    input_list = [str(writer.id) for writer in writers ]  # generate it as needed

    prefs = create_dynamic_checkbox(input_list)
    form = prefs(request.form)
    if form.validate_on_submit():
        
        writer_ids = [field.name for field in form if field.data is True]
        print(writer_ids)
        # store id in paid table
        paid_writers = User.query.join(Orders,  User.orders ).options(contains_eager(User.orders)).filter((Orders.status == Status.completed) & (User.id.in_(writer_ids))).all()

        # store id in paid table
        # for each writer fetch completed jobs
        
        set_orders_as_paid(paid_writers)
        # save in paid tables
        # update order status

        return render_template("admin/editor/unpaid_writers.html", writers = writers, form = form, zip=zip, db=db)

    return render_template("admin/editor/unpaid_writers.html", writers = writers, form = form, zip=zip, db=db)




# Return paid orders
###-----------------------------------------
@admin.route('/view_paid_orders', methods = ["GET", "POST"])
@login_required
def payment_history():
    payments = Payments.query.all()

    return render_template("admin/editor/payment_history.html", payments = payments)

# Return writers list
###-----------------------------------------
@admin.route('/view_writers', methods = ["GET", "POST"])
@login_required
def view_writers():
    writers = User.query.filter(User.user_type.in_([AccountType.ADMIN, AccountType.EDITOR])).all()

    return render_template("admin/editor/writers_list.html", writers = writers)




###-----------------------------------
def populate_bidding_form(order_id):
    writer_ids = BiddingOrders.query\
            .join(Bids, Bids.bidding_id==BiddingOrders.id)\
            .add_columns(Bids.writer_id)\
            .filter((BiddingOrders.order_id == order_id) & (BiddingOrders.id == Bids.bidding_id) ).all()
    ids = [writer.writer_id for writer in writer_ids ]
    

    bid_writers = User.query.filter(User.id.in_(ids)).all()
    
    if len(bid_writers) == 0:
        return [("None", "None")]
    else:
        return  [ (writer.id, writer.name) for writer in bid_writers ]




###_---------------------------------------------------------------------------
@admin.route('/admin_send_message?<order_id>', methods = ["GET", "POST"])
@login_required
def send_message(order_id):
    # get message
    
    # get recipient
    # save to database]
    
    # add file upload mechanism
    #order = Orders.query.get(order_id)

    message_form = AdminMessageForm()
    if message_form.validate_on_submit():
        order = Orders.query.get(order_id)
        

        
        message =  Messages(
            sender_id = session['user_id'],
            recipient_id = order.writer_id,
            subject = message_form.subject.data,
            order_id = order_id,
            message = message_form.message.data,
            sent_to = message_form.to_department.data,
            sent_from = message_form.from_department.data,
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
    else:
        print("Form not validated")
        flash("Form was not validated successfully")
    return redirect(url_for("admin.edit_order", order_id = order_id, _anchor='files'))



#-------------------------------------------------------------------------------------
@admin.route('/create_order', methods=["GET", "POST"])
@login_required
def create_order():
    form = OrderForm()
    if form.is_submitted():
        if form.validate_on_submit():
            order = Orders()
            order.paper_length = form.number_words.data
            order.page_words = form.length_type.data
            order.topic = form.topic.data
            order.description = form.description.data
            order.audience = form.audience.data
            order.medium = form.medium.data
            order.tone = form.tone.data
            order.person = form.person.data
            order.english_country = form.english_country.data
            order.example = form.example.data
            order.research_links = form.research_links.data
            order.seo = form.seo.data
            order.business_description = form.business_description.data
            order.comments = form.comments.data
            order.price = form.price.data
            order.customer_price = form.customer_price.data
            order.deadline = parse(form.deadline_date.data + " " + form.deadline_time.data)
            order.editor_id = session['user_id']
            order.order_status = form.order_status.data

            # create transaction
            transaction  = OrderTransactions(
                order = order,
                description = "Created order and set to status [{}]".format(order.order_status),
                editor_id = order.editor_id

            )
            # set order in relevant table
            
            operation = Operations[order.order_status](
                order = order,
                description = "Created order and set to status [{}]".format(order.order_status),
                editor_id = order.editor_id
            )
            
            try:
                db.session.add(order)
                db.session.add(transaction)
                db.session.add(operation)
                db.session.commit()
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("Failed to add customer")
                flash('Database Error: Failed to record order')
                print(e)
            else:
                # on successful saving
                flash(Markup('<a href="{}">Order #{}</a> was created and set to status [{}]. '.format(url_for('admin.edit_order', order_id = order.id), order.id, order.status.value)))
                return redirect(url_for('admin.create_order'))


    return render_template("admin/editor/create_order.html", order_form = form)

#-------------------------------------------------------------------------------------
@admin.route('/update_order?<order_id>', methods=["GET", "POST"])
@login_required
def update_order(order_id):
    form = OrderForm()
    if form.is_submitted():
        if form.validate_on_submit():
            order = Orders.query.get(order_id)
            order.paper_length = form.number_words.data
            order.page_words = form.length_type.data
            order.topic = form.topic.data
            order.description = form.description.data
            order.audience = form.audience.data
            order.medium = form.medium.data
            order.tone = form.tone.data
            order.person = form.person.data
            order.english_country = form.english_country.data
            order.example = form.example.data
            order.research_links = form.research_links.data
            order.seo = form.seo.data
            order.business_description = form.business_description.data
            order.comments = form.comments.data
            order.price = form.price.data
            order.customer_price = form.customer_price.data
            order.deadline = parse(form.deadline_date.data + " " + form.deadline_time.data)
            order.editor_id = session['user_id']
            order.order_status = form.order_status.data

            # create transaction
            transaction  = OrderTransactions(
                order = order,
                description = "Updated order and set to status [{}]".format(order.order_status),
                editor_id = order.editor_id

            )
            # set order in relevant table
            
            operation = Operations[order.order_status](
                order = order,
                description = "Updated order and set to status [{}]".format(order.order_status),
                editor_id = order.editor_id
            )
            
            try:
                db.session.add(order)
                db.session.add(transaction)
                db.session.add(operation)
                db.session.commit()
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("Failed to add customer")
                flash('Database Error: Failed to record order')
                print(e)
            else:
                # on successful saving
                flash(Markup('<a href="{}">Order details for #{}</a> was updated and set to status [{}]. '.format(url_for('admin.edit_order', order_id = order.id), order.id, order.status.value)))
                return redirect(url_for('admin.edit_order_details', order_id = order.id))


    return render_template("admin/editor/create_order.html", order_form = form)


####----------------------------------------------------------------------------------
@admin.route('/available_orders', methods = ['GET', 'POST'])
@login_required
def available_orders():
    
    orders = Orders.query.filter((Orders.status == Status.unassigned) | (Orders.status == Status.bid_status)).all()
        
    for order in orders:        
        order.difference = find_time_difference(order.deadline)

    return render_template("admin/editor/available_orders.html", orders = orders)

####----------------------------------------------------------------------------------
@admin.route('/admin_view_inbox', methods = ['GET', 'POST'])
@login_required
def view_inbox():
    page = request.args.get('page', 1, type=int)
    #user = User.query.filter(User.id == session['user_id'])
    messages = Messages.query.filter(Messages.sent_to.in_([Department.ADMIN, Department.EDITOR, Department.FINANCE, Department.QUALITY])).order_by(desc(Messages.timestamp)).paginate(page, current_app.config['POSTS_PER_PAGE'], False)



    next_url = url_for('admin.view_inbox',  page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('admin.view_inbox', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template("admin/editor/inbox.html", messages = messages.items, next_url=next_url, prev_url=prev_url)


####----------------------------------------------------------------------------------
@admin.route('/admin_view_outbox', methods = ['GET', 'POST'])
@login_required
def view_outbox():
    page = request.args.get('page', 1, type=int)
    #user = User.query.filter(User.id == session['user_id'])

    messages = Messages.query.filter((Messages.sent_from.in_([Department.ADMIN, Department.EDITOR, Department.FINANCE, Department.QUALITY])) & (Messages.thread_status == ThreadStatus.PARENT)).order_by(desc(Messages.timestamp)).paginate(page, 10, False)

    prev_url, next_url = return_page_links(messages, 'admin.view_outbox')

    #messages = current_user.messages_sent.order_by(Messages.timestamp.desc()).all()
    return render_template("admin/editor/outbox.html", messages = messages.items, next_url=next_url, prev_url=prev_url)




#-view all messages
####-------------------------------------------------------------------------
@admin.route('/admin_view_message?<message_id>', methods = ['GET', 'POST'])
@login_required
def view_message(message_id):
    """Renders view for a single message"""
    # fetch customer by ID/ primary key
    message = Messages.query.options(joinedload(Messages.order)).get(message_id)
    order = message.order

    form = AssignForm()
    if order.status == Status.bid_status:
        form.bid_writers.choices = populate_bidding_form(order.id)
    else:
        form.bid_writers.choices = [('1','None')]
    form.writer_name.choices = [(g.id, g.name) for g in User.query.filter((User.user_type == AccountType.WRITER)).all()]  

    order.time_remaining = find_time_difference(order.deadline)

    file_form = FileForm()
    message_form = ReplyMessageForm(order_id = order.id, thread_id = message.id)
    
    messages = Messages.query.filter(Messages.thread_id == message_id).order_by(desc(Messages.timestamp)).all()

    return render_template("admin/editor/order_message_single.html", order= order, assign_form = form, file_form = file_form, message_form = message_form, detailed_message = message, messages = messages)




#-reply to a message order from order form
####-------------------------------------------------------------------------
@admin.route('/reply_order_message', methods = ['GET', 'POST'])
@login_required
def reply_order_message():
    message_form = ReplyMessageForm()
    if message_form.validate_on_submit():
        parent_message = Messages.query.get(message_form.thread_id.data)
        order = Orders.query.get(message_form.order_id.data)
        

        
        message =  Messages(
            sender_id = session['user_id'],
            recipient_id = order.writer_id,
            thread_id = message_form.thread_id.data,
            subject = parent_message.subject,
            order_id = message_form.order_id.data,
            message = message_form.message.data,
            sent_to = parent_message.sent_to,
            sent_from = message_form.from_department.data,
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
    return redirect(url_for("admin.edit_order", order_id = order.id, _anchor='files'))




#-view message detail
####-------------------------------------------------------------------------
@admin.route('/admin_view_message_detail?<message_id>', methods = ['GET', 'POST'])
@login_required
def view_message_detail(message_id):
    page = request.args.get('page', 1, type=int)

    threaded_messages = Messages.query.filter((Messages.thread_id == message_id)).order_by(desc(Messages.timestamp)).paginate(page, 10, False)
    message = Messages.query.get(message_id)

    #messages = Messages.query.join(ThreadedMessages).filter(ThreadedMessages.sent_to.in_([Department.ADMIN, Department.EDITOR, Department.FINANCE, Department.QUALITY])).paginate(page, 10, False)
    


    return render_template("admin/editor/message_detail.html", message = message, threaded_messages = threaded_messages.items)



#-view compose email view
####-------------------------------------------------------------------------
@admin.route('/compose_email', methods = ['GET', 'POST'])
@login_required
def compose_email():
    message_form = AdminMessageForm()

    return render_template("admin/editor/email_compose.html", message_form = message_form)




####-------------------------------------------------------------------------
@admin.route('/compose_admin_email', methods = ['GET', 'POST'])
@login_required
def compose_admin_message():
    message_form = AdminMessageForm()
    if message_form.validate_on_submit():
        
        message =  Messages(
            sender_id = session['user_id'],
            subject = message_form.subject.data,
            message = message_form.message.data,
            sent_to = message_form.to_department.data,
            sent_from = message_form.from_department.data,
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
            return redirect(url_for('admin.compose_email'))
    else:
        print("Form not validated")
        flash("Form was not validated successfully")
    return render_template("admin/editor/email_compose.html", message_form = message_form)


# delete messages from the main outbox
####-------------------------------------------------------------------------
@admin.route('/delete_admin_email?<message_id>', methods = ['GET', 'POST'])
@login_required
def delete_admin_message(message_id):
    message = Messages.query.get(message_id)
    message.thread_status = ThreadStatus.DELETED
    try:
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        flash('Error: Message was not deleted')
        print(e)
    else:
        # on successful saving

        msg = f"Message was moved to <a href='{url_for('admin.view_trash')}'>Trash</a>"
        
        flash(Markup(msg))
    
    return redirect(url_for('admin.view_outbox'))

####----------------------------------------------------------------------------------
@admin.route('/admin_view_trash', methods = ['GET', 'POST'])
@login_required
def view_trash():
    page = request.args.get('page', 1, type=int)
    
    messages = Messages.query.filter((Messages.sent_from.in_([Department.ADMIN, Department.EDITOR, Department.FINANCE, Department.QUALITY])) & (Messages.thread_status == ThreadStatus.DELETED)).order_by(desc(Messages.timestamp)).paginate(page, 10, False)

    
    return render_template("admin/editor/trash.html", messages = messages.items)




    

##########################################################
##########################################################
##########################################################
##########################################################
##########################################################
##########################################################
##########################################################
##########################################################
##########################################################
##########################################################

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
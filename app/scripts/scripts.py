
import os
import datetime
import re
from time import time

from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import session

from flask import Markup
from dateutil.parser import parse
from werkzeug.security import generate_password_hash



from app.models import CurrentOrders, BiddingOrders, UnassignedOrders, PaidOrders, RevisionOrders, CompletedOrders, PaidOrders, FinishedOrders, OrderTransactions, Writers, Status, Payments

from app import db
from app.emails import send_message, send_admin_message, send_customer_message
from app.forms import AssignForm, DepositForm, LoginForm, OrderForm, AssignForm
from app.mpesa import send_money_request




def set_order_progress(order, action, writer_id, writer_name):
    reassign = False
    # check if order has an entry in writers table
    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.paid, Status.completed]:
        reassign = True
        print(current_writer)
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )


    # update current order
    order.status = action
    order.writer_id = writer_id
    order.editor_id = session['user_id']

    # update current writer table
    current_order = CurrentOrders(
        description = "Assign Order to {}".format( writer_name),
        editor_id = session['user_id'], 
        writer_id = writer_id,
        order  = order

    )

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order assigned to [{}] Current status: [{}]".format(writer_name, order.status),
        editor_id = order.editor_id,
        writer_id = writer_id

    )


    try:
        #db.session.add(current_writer)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(order)
        db.session.add(current_order)
        db.session.add(transaction)
        db.session.add(writer)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to assign order")
        flash('Database Error: Failed to assign order')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)
        msg = "Order was assigned successfully to {}".format( writer_name)
        flash(msg)





#-----------------------------------------------------------------------
def set_bidding_status(order, action, writer_id, writer_name):
    reassign = False
        # check if order has an entry in writers table
    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )    
    # update current action
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.paid, Status.completed]:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )

    order.status = action
    order.writer_id = None
    bidding_order = BiddingOrders(
        description = "Set Order to status [Bidding]",
        editor_id = session['user_id'],
        order = order 

    )
    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id

    )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(bidding_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set status")
        flash('Database Error: Failed to set order status to bidding')
        logging.DEBUG(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)
        
        msg = "Order successfuly set to [Bidding status]"
        flash(msg)





######-------------------------------------------------------------
def set_order_unassigned(order, action, writer_id, writer_name):
    reassign = False

    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )    
    # update current action
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.paid, Status.completed]:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )

    order.status = action
    order.writer_id = None

    unassigned_order = UnassignedOrders(
        description = "Order set to unassigned status by {}".format(session['user_id'] ),
        editor_id = session['user_id'], 
    )

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(unassigned_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to unassign order")
        flash('Database Error: Failed to unassign order')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Order was unassigned successfully. Current status: [{}]".format( action)
        flash(msg)





#---------------------------------------------------------------------------
def set_order_reassigned(order, action, writer_id, writer_name):
    
    reassign = False

    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )    
    # update current action
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.completed, Status.paid]:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )

    order.status = action
    

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to unassign order")
        flash('Database Error: Failed to unassign order')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Order was reassigned successfully. Current status: [{}]".format( action)
        flash(msg)



##---------------------------------------------------------
def set_order_completed(order, action, writer_id, writer_name):
    
    reassign = False
    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            ) 
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.completed, Status.paid] and order.writer_id != writer_id:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )
    order.status = action
    order.writer_id = writer_id

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )
    # create completed order
    completed_order = CompletedOrders(
        order = order,
        description = "Order completed by:[{}] Current status: [{}]".format(order.writer.name, action),
        editor_id = session['user_id'],
        )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(completed_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set order status to [Complete]")
        flash('Database Error: Failed to set order status to [Complete]"')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Order was completed successfully by {}. Current status: [{}]".format(order.writer.name, action)
        flash(msg)



###-----------------------------------------------------------------------------
def set_order_revision(order, action, writer_id, writer_name):

    reassign = False

    current_writer = Writers.query.filter((Writers.writers_id == order.writer_id) & (Writers.order == order)).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.completed, Status.paid] and order.writer_id != writer_id:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )
    order.status = action
    order.writer_id = writer_id

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )
    # create revision order
    revision_order = RevisionOrders(
        order = order,
        description = "Order set to [revision status] Current Writer: [{}]".format(writer_name),
        editor_id = session['user_id'],
        )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(revision_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set order status to [Revision]")
        flash('Database Error: Failed to set order status to [Revision]"')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Order set to [revision status] Current Writer: [{}]".format(writer_name, action)
        flash(msg)




###------------------------------------------------------------------------
def set_order_finished(order, action, writer_id, writer_name):
    reassign = False

    current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.completed, Status.paid] and order.writer_id != writer_id:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )
    order.status = action
    order.writer_id = writer_id

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )
    # create revision order
    finished_order = FinishedOrders(
        order = order,
        description = "Order set to [Finished status] Current Writer: [{}]".format(writer_name),
        editor_id = session['user_id'],
        )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(finished_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set order status to [Complete]")
        flash('Database Error: Failed to set order status to [Complete]"')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Order set to [FINISHED status] Current Writer: [{}]".format(writer_name, action)
        flash(msg)



#####------------------------------------------------------------------------
def set_order_paid(order, action, writer_id, writer_name):

    reassign = False

    current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
    if current_writer is None:
        # create writer entry for the order
            # update writers table
        writer = Writers(
            writers_id = writer_id,
            order = order,
            job_status = order.status
            )
    elif order.status in [Status.progress, Status.revision, Status.finished, Status.completed, Status.paid] and order.writer_id != writer_id:
        reassign = True

        current_writer = Writers.query.filter(Writers.writers_id == order.writer_id and Writers.order == order).first()
        current_writer.job_status = Status.reassigned
        
        # create transaction
        recent_transaction  = OrderTransactions(
            order = order,
            description = "Order reassigned from [{}] Current status: [{}]".format(current_writer.writer.name, action),
            editor_id = session['user_id'],
            writer_id = writer_id
            )
    order.status = action
    order.writer_id = writer_id

    # create transaction
    transaction  = OrderTransactions(
        order = order,
        description = "Order set to status [{}]".format(order.status),
        editor_id = order.editor_id,
        writer_id = None

    )
    # create paid order
    paid_order = PaidOrders(
        order = order,
        description = "Payment for order #{} by Writer: [{}] completed".format(order.id,writer_name),
        editor_id = session['user_id'],
        )

    try:
        db.session.add(order)
        if reassign:
            db.session.add(recent_transaction)
        db.session.add(paid_order)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set order status to [Paid]")
        flash('Database Error: Failed to set order status to [Paid]"')
        print(e)
    else:
        # on successful saving
        if reassign:
            msg = "Order reassigned from {}".format(current_writer.writer.name)
            flash(msg)

        msg = "Payment status for Order #{} done by Writer: [{}] is completed".format(order.id, writer_name)
        flash(msg)




#####-----actions
Actions = {
    "unassigned" : set_order_unassigned,
    "bid_status" : set_bidding_status,
    "progress" : set_order_progress,
    "reassigned" : set_order_reassigned,
    "completed" : set_order_completed,
    "revision" : set_order_revision,
    "finished" : set_order_finished,
    "paid" : set_order_paid
}

Operations = {
    "unassigned" : UnassignedOrders,
    "bid_status" : BiddingOrders,
    "progress" : CurrentOrders,
    "reassigned" : "",
    "completed" : CompletedOrders,
    "revision" : RevisionOrders,
    "finished" : FinishedOrders,
    "paid" : PaidOrders
}

def set_orders_as_paid(paid_writers):
    # create transaction
    now = datetime.datetime.now()
    payment_time = now.strftime("%Y-%m-%d %H:%M:%S")

    transactions = []
    orders_processed = 0

    for writer in paid_writers:
        

        orders = writer.orders

        # create payment object
        payment = Payments(
            writer_id = writer.id,
            payment_date = now.strftime("%Y-%m-%d %H:%M:%S"),
            description = f"Payment on {payment_time}",
            amount_paid = sum([ order.price for order in orders ])
        )
        
        orders_processed = len(orders) + orders_processed
        for order in orders:

            order.status = Status.paid

            transaction  = OrderTransactions(
                order = order,
                description = "Order set to status [{}]".format(order.status),
                editor_id = order.editor_id,
                writer_id = None

            
            
            )
            transactions.append(transaction)
            # create paid order
            paid_order = PaidOrders(
                order = order,
                description = "Payment for order #{} by Writer: [{}] completed".format(order.id,writer.name),
                editor_id = session['user_id'],
                payment = payment
                )
            transactions.append(paid_order)
        transactions.append(payment)

    try:
        db.session.bulk_save_objects(transactions)
        db.session.commit()
    except Exception as e:
        # for resetting non-commited .add()
        db.session.rollback()
        db.session.flush()
        print("Failed to set orders as [Paid]")
        flash('Database Error: Failed to set orders as [Paid]"')
        print(e)
    else:

        msg = f"{orders_processed} Orders were marked as paid"
        flash(msg)

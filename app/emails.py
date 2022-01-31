from flask import Flask
from flask_mail import Mail
from flask_mail import Message

from . import mail




def send_message():
    msg = Message('Hello from the other side!', sender = 'clairekanini@gmail.com', recipients = ['paul@mailtrap.io'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    print("Sending message")
    mail.send(msg)

def send_customer_message(customer_email, transaction_subject, transaction_message):
    msg = Message(transaction_subject, sender = 'info@mifbanks.co.ke', recipients = [f'{customer_email}'])
    msg.body = transaction_message
    mail.send(msg)

def send_admin_message(transaction_subject, transaction_message):
    msg = Message(transaction_subject, sender = 'info@mifbanks.co.ke', recipients = ['admin_email@gmail.com'])
    msg.body = transaction_message
    mail.send(msg)

def send_user_signup_mail(customer_email, customer_name):
    msg = Message('Welcome to your new MIFS Account', sender = 'info@mifbanks.co.ke', recipients = [f'{customer_email}'])
    msg.body = "Hey "+ f'{customer_name}' + "thank you for signing up to MIFS Trust Bank Digital Platform. Click this link to verify your email"
    print("Sending message")
    mail.send(msg)
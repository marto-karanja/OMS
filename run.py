#!/usr/bin/env python
import os

from app import create_app, db
from app.models import User, AccountType, Orders, Status, Length_type


#from flask_script import Manager, Shell
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
application = app
#manager = Manager(app)
migrate = Migrate(application, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=application, db=db)

#---------------------------------
@app.cli.command('db_seed')
def db_seed():
    writer1 = User(email = 'kmmartozz@outlook.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'John Omondi', user_type = AccountType.WRITER)
    writer2 = User(email = 'kmmartozz@gmail.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'Carol Karoke', user_type = AccountType.WRITER)
    writer3 = User(email = 'hireessaywriters@gmail.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'Phillip Njoroge', user_type = AccountType.WRITER)
    writer4 = User(email = 'hireessayriters@gmail.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'Jane Wambui', user_type = AccountType.WRITER)
    editor = User(email = 'kilungubenson78@gmail.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'Hassan Musa', user_type = AccountType.EDITOR)
    admin = User(email = 'admin@writersgigs.com', password = 'sha256$CAblJ1N2fSbUPFcs$9132b66a42f5e3ed314f20cdfc129211f319a0e8cd2de8cfe49002c32a3ce6b8', number = '0727531915', name = 'Kush Allan', user_type = AccountType.ADMIN)

    ## create orders
    order1 = Orders(
        paper_length = '3',
        page_words = Length_type.PAGES,
        topic = 'Top 3 cars 2021',
        description = 'Car Sales',
        audience = 'Enthusiasts',
        medium = 'Blog Post',
        tone = 'Casual',
        person = 'SECOND',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = 'url.to.everywhere, url.to.knowhere',
        seo = 'all, seo',
        business_description = '',
        comments = 'yes',
        status = Status.unassigned,
        price = '3494.00',
        deadline = '2022-05-24 02:00:00',
        editor = admin
    )

    order2= Orders(
        paper_length = '250',
        page_words = Length_type.WORDS,
        topic = 'brief summary',
        description = "description of the paper\nbrief summary",
        audience = 'technical',
        medium = 'landing page copy',
        tone = 'Formal',
        person = 'FIRST',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = "url.to.everywhere\nurl.to.everywhere\nurl.to.everywhere",
        seo = 'brief, summary',
        business_description = '',
        comments = 'yes',
        status = Status.unassigned,
        price = '280.00',
        deadline = '2022-06-23 03:00:00',
        editor = admin
    )

    order3 = Orders(
        paper_length = '1000',
        page_words = Length_type.WORDS,
        topic = 'Decline of Big 5 in Africa',
        description = 'Decline of big 5, rise of poaching',
        audience = 'Tourists',
        medium = 'Quora response',
        tone = 'Descriptive',
        person = 'THIRD',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = 'url.to.everywhere, url.to.knowhere',
        seo = 'big 5, cat',
        business_description = '',
        comments = '',
        status = Status.unassigned,
        price = '1200.00',
        deadline = '2022-05-28 02:30:00',
        editor = admin
    )

    order4 = Orders(
        paper_length = '1000',
        page_words = Length_type.WORDS,
        topic = 'New blog topic',
        description = """
                        class Parent(Base):
                            __tablename__ = 'parent'
                            id = Column(Integer, primary_key=True)
                            children = relationship("Child")

                        class Child(Base):
                            __tablename__ = 'child'
                            id = Column(Integer, primary_key=True)
                            parent_id = Column(Integer, ForeignKey('parent.id'))',""",
        audience = 'Tourists',
        medium = 'Quora response',
        tone = 'Descriptive',
        person = 'THIRD',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = 'url.to.everywhere, url.to.knowhere',
        seo = 'big 5, cat',
        business_description = '',
        comments = '',
        status = Status.unassigned,
        price = '1200.00',
        deadline = '2022-05-25 02:30:00',
        editor = admin
    )

    order5 = Orders(
        paper_length = '300',
        page_words = Length_type.WORDS,
        topic = 'Cooking recipes',
        description = """
                        class User(UserMixin, db.Model):
                        # ...
                        messages_sent = db.relationship('Message',
                                                        foreign_keys='Message.sender_id',
                                                        backref='author', lazy='dynamic')
                        messages_received = db.relationship('Message',
                                                            foreign_keys='Message.recipient_id',
                                                            backref='recipient', lazy='dynamic')
                        last_message_read_time = db.Column(db.DateTime)

                        # ...

                        def new_messages(self):
                            last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
                            return Message.query.filter_by(recipient=self).filter(
                                Message.timestamp > last_read_time).count()""",
        audience = 'Cooks',
        medium = 'Quora response',
        tone = 'Descriptive',
        person = 'THIRD',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = 'url.to.everywhere, url.to.knowhere',
        seo = 'big 5, cat',
        business_description = '',
        comments = '',
        status = Status.unassigned,
        price = '1200.00',
        deadline = '2022-05-22 02:30:00',
        editor = admin
    )
    
    order6 = Orders(
        paper_length = '500',
        page_words = Length_type.WORDS,
        topic = 'Cooking recipes',
        description = """
                        Now that we have two tables, we will see how to create queries on both tables at the same time. To construct a simple implicit join between Customer and Invoice, we can use Query.filter() to equate their related columns together. Below, we load the Customer and Invoice entities at once using this method −

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

for c, i in session.query(Customer, Invoice).filter(Customer.id == Invoice.custid).all():
   print ("ID: {} Name: {} Invoice No: {} Amount: {}".format(c.id,c.name, i.invno, i.amount))

The SQL expression emitted by SQLAlchemy is as follows −

SELECT customers.id 
AS customers_id, customers.name 
AS customers_name, customers.address 
AS customers_address, customers.email 
AS customers_email, invoices.id 
AS invoices_id, invoices.custid 
AS invoices_custid, invoices.invno 
AS invoices_invno, invoices.amount 
AS invoices_amount
FROM customers, invoices
WHERE customers.id = invoices.custid

And the result of the above lines of code is as follows −

ID: 2 Name: Gopal Krishna Invoice No: 10 Amount: 15000
ID: 2 Name: Gopal Krishna Invoice No: 14 Amount: 3850
ID: 3 Name: Govind Pant Invoice No: 3 Amount: 10000
ID: 3 Name: Govind Pant Invoice No: 4 Amount: 5000
ID: 4 Name: Govind Kala Invoice No: 7 Amount: 12000
ID: 4 Name: Govind Kala Invoice No: 8 Amount: 8500
ID: 5 Name: Abdul Rahman Invoice No: 9 Amount: 15000
ID: 5 Name: Abdul Rahman Invoice No: 11 Amount: 6000

The actual SQL JOIN syntax is easily achieved using the Query.join() method as follows −

session.query(Customer).join(Invoice).filter(Invoice.amount == 8500).all()""",
        audience = 'Cooks',
        medium = 'Quora response',
        tone = 'Descriptive',
        person = 'THIRD',
        english_country = 'US',
        example = 'url.to.everywhere',
        research_links = 'url.to.everywhere, url.to.knowhere',
        seo = 'big 5, cat',
        business_description = '',
        comments = '',
        status = Status.unassigned,
        price = '1200.00',
        deadline = '2022-06-23 01:30:00',
        editor = admin
    )



    db.session.add(writer1)
    db.session.add(writer2)
    db.session.add(writer3)
    db.session.add(writer4)
    db.session.add(editor)
    db.session.add(admin)
    """
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)"""

    db.session.commit()
    print('Database seeded!')

"""
def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run() """

if __name__ == '__main__':
    application.run()
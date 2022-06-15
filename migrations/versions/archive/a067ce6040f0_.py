"""empty message

Revision ID: a067ce6040f0
Revises: 5841c15b41de
Create Date: 2022-03-24 02:24:08.896075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a067ce6040f0'
down_revision = '5841c15b41de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('number', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('user_type', sa.Enum('EDITOR', 'WRITER', 'ADMIN', name='accounttype'), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
    sa.Column('mobile', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=100), nullable=True),
    sa.Column('account_type', sa.String(length=100), nullable=True),
    sa.Column('branch', sa.String(length=50), nullable=True),
    sa.Column('bank_balance', sa.Float(precision=2), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_words', sa.String(length=300), nullable=True),
    sa.Column('topic', sa.String(length=1000), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('audience', sa.String(length=1000), nullable=True),
    sa.Column('medium', sa.String(length=1000), nullable=True),
    sa.Column('tone', sa.String(length=1000), nullable=True),
    sa.Column('person', sa.Enum('FIRST', 'SECOND', 'THIRD', name='person'), nullable=True),
    sa.Column('english_country', sa.Enum('UK', 'US', 'AUSTRALIA', name='englishcountry'), nullable=True),
    sa.Column('example', sa.String(length=1000), nullable=True),
    sa.Column('research_links', sa.Text(), nullable=True),
    sa.Column('seo', sa.String(length=1000), nullable=True),
    sa.Column('business_description', sa.Text(), nullable=True),
    sa.Column('comments', sa.String(length=1000), nullable=True),
    sa.Column('status', sa.Enum('unassigned', 'bid_status', 'progress', 'reassigned', 'completed', 'revision', 'finished', 'paid', name='status'), server_default='unassigned', nullable=False),
    sa.Column('price', sa.Numeric(precision=65, scale=2), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_editor_id'), 'orders', ['editor_id'], unique=False)
    op.create_index(op.f('ix_orders_writer_id'), 'orders', ['writer_id'], unique=False)
    op.create_table('bidding_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('completed_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('current_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('file_location', sa.String(length=1000), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('type', sa.Enum('CUSTOMER', 'WRITER', 'EDITOR', name='order_type'), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_orders_last_edited'), 'file_orders', ['last_edited'], unique=False)
    op.create_table('finished_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('recipient', sa.Enum('WRITER', 'FINANCE', 'QUALITY', 'CUSTOMER', name='recipient'), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    op.create_table('order_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paid_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revision_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(precision=2), nullable=True),
    sa.Column('transaction_identifier', sa.String(length=100), nullable=True),
    sa.Column('transaction_type', sa.Enum('CREDIT', 'DEBIT', name='transactiontype'), nullable=True),
    sa.Column('transaction_time', sa.DateTime(), nullable=True),
    sa.Column('transaction_method', sa.Enum('CASH', 'MPESA', 'CREDIT_CARD', 'DEBIT_CARD', name='transactionmethod'), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unassigned_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('editor_id', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('writers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('writers_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('job_status', sa.Enum('unassigned', 'bid_status', 'progress', 'reassigned', 'completed', 'revision', 'finished', 'paid', name='status'), nullable=True),
    sa.Column('rating', sa.String(length=1000), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_edited', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['writers_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bidding_id', sa.Integer(), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bidding_id'], ['bidding_orders.id'], ),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bids')
    op.drop_table('writers')
    op.drop_table('unassigned_orders')
    op.drop_table('transactions')
    op.drop_table('revision_orders')
    op.drop_table('paid_orders')
    op.drop_table('order_transactions')
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('finished_orders')
    op.drop_index(op.f('ix_file_orders_last_edited'), table_name='file_orders')
    op.drop_table('file_orders')
    op.drop_table('current_orders')
    op.drop_table('completed_orders')
    op.drop_table('bidding_orders')
    op.drop_index(op.f('ix_orders_writer_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_editor_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_table('customers')
    op.drop_table('user')
    # ### end Alembic commands ###

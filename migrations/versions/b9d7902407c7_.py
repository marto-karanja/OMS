"""empty message

Revision ID: b9d7902407c7
Revises: d91eeb5a8ef2
Create Date: 2022-08-21 00:12:42.281539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b9d7902407c7'
down_revision = 'd91eeb5a8ef2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('writer_id', sa.Integer(), nullable=True),
    sa.Column('payment_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('amount_paid', sa.Numeric(precision=65, scale=2), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_threaded_messages_timestamp', table_name='threaded_messages')
    op.drop_table('threaded_messages')
    op.add_column('messages', sa.Column('message', sa.Text(), nullable=True))
    op.add_column('messages', sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('messages', sa.Column('sent_to', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN', name='department'), nullable=True))
    op.add_column('messages', sa.Column('sent_from', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN', name='department'), nullable=True))
    op.add_column('messages', sa.Column('thread_status', sa.Enum('PARENT', 'CHILD', name='threadstatus'), server_default='CHILD', nullable=True))
    op.create_index(op.f('ix_messages_order_id'), 'messages', ['order_id'], unique=False)
    op.create_index(op.f('ix_messages_recipient_id'), 'messages', ['recipient_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)
    op.create_index(op.f('ix_messages_sent_from'), 'messages', ['sent_from'], unique=False)
    op.create_index(op.f('ix_messages_sent_to'), 'messages', ['sent_to'], unique=False)
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    op.add_column('orders', sa.Column('paper_length', sa.Float(), nullable=True))
    op.add_column('orders', sa.Column('page_words', sa.Enum('WORDS', 'PAGES', name='length_type'), nullable=True))
    op.drop_column('orders', 'number_words')
    op.add_column('paid_orders', sa.Column('payment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'paid_orders', 'payments', ['payment_id'], ['id'])
    op.add_column('user', sa.Column('date_joined', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_joined')
    op.drop_constraint(None, 'paid_orders', type_='foreignkey')
    op.drop_column('paid_orders', 'payment_id')
    op.add_column('orders', sa.Column('number_words', mysql.VARCHAR(collation='utf8mb4_bin', length=300), nullable=True))
    op.drop_column('orders', 'page_words')
    op.drop_column('orders', 'paper_length')
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_index(op.f('ix_messages_sent_to'), table_name='messages')
    op.drop_index(op.f('ix_messages_sent_from'), table_name='messages')
    op.drop_index(op.f('ix_messages_sender_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_recipient_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_order_id'), table_name='messages')
    op.drop_column('messages', 'thread_status')
    op.drop_column('messages', 'sent_from')
    op.drop_column('messages', 'sent_to')
    op.drop_column('messages', 'timestamp')
    op.drop_column('messages', 'message')
    op.create_table('threaded_messages',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('message', mysql.TEXT(collation='utf8mb4_bin'), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('sent_to', mysql.ENUM('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN'), nullable=True),
    sa.Column('sent_from', mysql.ENUM('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN'), nullable=True),
    sa.Column('thread_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['messages.id'], name='threaded_messages_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_bin',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_threaded_messages_timestamp', 'threaded_messages', ['timestamp'], unique=False)
    op.drop_table('payments')
    # ### end Alembic commands ###
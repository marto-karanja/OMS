"""empty message

Revision ID: ce6b86fb129b
Revises: 6365a918aa2d
Create Date: 2022-05-21 18:20:44.157689

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ce6b86fb129b'
down_revision = '6365a918aa2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('page_words', sa.Enum('WORDS', 'PAGES', name='length_type'), nullable=True))
    op.drop_column('orders', 'number_words')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('number_words', mysql.VARCHAR(collation='utf8mb4_bin', length=300), nullable=True))
    op.drop_column('orders', 'page_words')
    # ### end Alembic commands ###

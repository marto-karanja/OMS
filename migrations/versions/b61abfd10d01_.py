"""empty message

Revision ID: b61abfd10d01
Revises: 6d6c989afce7
Create Date: 2022-05-23 09:03:11.532216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b61abfd10d01'
down_revision = '6d6c989afce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_joined', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_joined')
    # ### end Alembic commands ###

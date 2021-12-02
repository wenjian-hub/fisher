"""empty message

Revision ID: 3bee52c516f8
Revises: dabf33934a52
Create Date: 2021-11-28 15:07:46.293679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3bee52c516f8'
down_revision = 'dabf33934a52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'create_time')
    op.drop_column('gift', 'create_time')
    op.drop_column('wish', 'create_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wish', sa.Column('create_time', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('gift', sa.Column('create_time', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('book', sa.Column('create_time', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
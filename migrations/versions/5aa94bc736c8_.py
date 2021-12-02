"""empty message

Revision ID: 5aa94bc736c8
Revises: 3bee52c516f8
Create Date: 2021-11-28 15:09:20.567614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5aa94bc736c8'
down_revision = '3bee52c516f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('create_time', sa.Integer(), nullable=False))
    op.add_column('gift', sa.Column('create_time', sa.Integer(), nullable=False))
    op.alter_column('user', 'create_time',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.add_column('wish', sa.Column('create_time', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wish', 'create_time')
    op.alter_column('user', 'create_time',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_column('gift', 'create_time')
    op.drop_column('book', 'create_time')
    # ### end Alembic commands ###
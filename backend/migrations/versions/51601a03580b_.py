"""empty message

Revision ID: 51601a03580b
Revises: 12d87167c78c
Create Date: 2024-06-02 14:37:30.106359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51601a03580b'
down_revision = '12d87167c78c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('token')
        batch_op.drop_column('token')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', mysql.VARCHAR(length=255), nullable=True))
        batch_op.create_index('token', ['token'], unique=True)

    # ### end Alembic commands ###
"""empty message

Revision ID: 4f818e77bc84
Revises: a53132534421
Create Date: 2024-05-29 11:45:57.108701

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f818e77bc84'
down_revision = 'a53132534421'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('finding_lost_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.drop_column('time_of_discovery')
        batch_op.drop_column('location_of_discovery')

    with op.batch_alter_table('report_lost_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.drop_column('time_of_discovery')
        batch_op.drop_column('location_of_discovery')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report_lost_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_of_discovery', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('time_of_discovery', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('time')
        batch_op.drop_column('location')

    with op.batch_alter_table('finding_lost_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_of_discovery', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('time_of_discovery', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('time')
        batch_op.drop_column('location')

    # ### end Alembic commands ###
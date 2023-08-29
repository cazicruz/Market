"""initial migration

Revision ID: 2159c907cd15
Revises: 
Create Date: 2023-08-23 23:24:10.338271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2159c907cd15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transaction_id', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_orders', schema=None) as batch_op:
        batch_op.drop_column('transaction_id')

    # ### end Alembic commands ###
"""Add screenshot to db

Revision ID: 10f14c7512f1
Revises: 8aacd1158993
Create Date: 2023-07-04 15:20:40.957833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10f14c7512f1'
down_revision = '8aacd1158993'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('screenshot', sa.PickleType(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_column('screenshot')

    # ### end Alembic commands ###

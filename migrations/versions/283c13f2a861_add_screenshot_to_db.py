"""Add screenshot to db

Revision ID: 283c13f2a861
Revises: 10f14c7512f1
Create Date: 2023-07-04 17:27:27.729611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283c13f2a861'
down_revision = '10f14c7512f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'using', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
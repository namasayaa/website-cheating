"""Add Screenshot Class db

Revision ID: 303ac15db656
Revises: 283c13f2a861
Create Date: 2023-07-04 19:56:45.181500

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '303ac15db656'
down_revision = '283c13f2a861'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_constraint('history_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('screenshot')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('screenshot', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('history_user_id_fkey', 'using', ['user_id'], ['id'])

    # ### end Alembic commands ###

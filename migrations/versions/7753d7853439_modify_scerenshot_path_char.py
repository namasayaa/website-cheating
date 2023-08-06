"""Modify Scerenshot path char

Revision ID: 7753d7853439
Revises: 303ac15db656
Create Date: 2023-07-04 20:17:51.682630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7753d7853439'
down_revision = '303ac15db656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('screenshot', schema=None) as batch_op:
        batch_op.alter_column('path',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=640),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('screenshot', schema=None) as batch_op:
        batch_op.alter_column('path',
               existing_type=sa.String(length=640),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###

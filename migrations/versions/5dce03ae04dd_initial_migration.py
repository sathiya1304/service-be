"""Initial migration

Revision ID: 5dce03ae04dd
Revises: 146ce6b824d8
Create Date: 2024-12-25 16:21:39.675828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5dce03ae04dd'
down_revision = '146ce6b824d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.alter_column('parent_category_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.alter_column('parent_category_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###

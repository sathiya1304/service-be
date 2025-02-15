"""Initial migration

Revision ID: c9f441af178c
Revises: af299a5a2428
Create Date: 2024-12-20 13:24:24.270479

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c9f441af178c'
down_revision = 'af299a5a2428'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_login',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email_id', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='MyISAM'
    )
    op.drop_table('admin_login')
    # ### end Alembic commands ###

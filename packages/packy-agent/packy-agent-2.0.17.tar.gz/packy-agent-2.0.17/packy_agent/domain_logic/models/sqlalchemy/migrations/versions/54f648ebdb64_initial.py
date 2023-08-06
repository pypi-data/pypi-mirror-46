"""initial

Revision ID: 54f648ebdb64
Revises: 
Create Date: 2018-08-25 17:58:51.997145

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '54f648ebdb64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'measurement',
        sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'),
                  autoincrement=True, nullable=False),
        sa.Column('measurement_type', sa.Integer(), nullable=False),
        sa.Column('created_at_ts', sa.Integer(), nullable=False),
        sa.Column('submitted_at_ts', sa.Integer(), nullable=True),
        sa.Column('error_at_ts', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.UnicodeText, nullable=True),
        sa.Column('value', sa.BLOB, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('measurement')

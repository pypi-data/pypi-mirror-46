"""empty message

Revision ID: fa9a67d72a78
Revises: 54f648ebdb64
Create Date: 2019-01-02 15:17:48.104469

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fa9a67d72a78'
down_revision = '54f648ebdb64'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('measurement', sa.Column('error_side', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('measurement', 'error_side')

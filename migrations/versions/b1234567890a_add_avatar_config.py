"""add avatar_config

Revision ID: b1234567890a
Revises: aef7119e6324
Create Date: 2026-06-16 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1234567890a'
down_revision = 'aef7119e6324'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_config', sa.String(length=512), server_default='{"body":"#2196F3","arms":"#4CAF50","legs":"#FFC107"}', nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('avatar_config')

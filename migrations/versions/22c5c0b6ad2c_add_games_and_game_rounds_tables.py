"""add games and game_rounds tables if not exist

Revision ID: 22c5c0b6ad2c
Revises: 3ce875da921a
Create Date: 2026-11-01 20:14:03.981042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c5c0b6ad2c'
down_revision = '3ce875da921a'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'games' not in existing_tables:
        op.create_table('games',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('room_code', sa.String(length=16), nullable=False),
            sa.Column('player1_id', sa.Integer(), nullable=False),
            sa.Column('player2_id', sa.Integer(), nullable=True),
            sa.Column('player1_score', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('player2_score', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('status', sa.String(length=32), nullable=False, server_default='waiting'),
            sa.Column('winner_id', sa.Integer(), nullable=True),
            sa.Column('current_round_num', sa.Integer(), nullable=False, server_default='1'),
            sa.Column('target_score', sa.Integer(), nullable=False, server_default='3'),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['player1_id'], ['users.id'], ),
            sa.ForeignKeyConstraint(['player2_id'], ['users.id'], ),
            sa.ForeignKeyConstraint(['winner_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('room_code')
        )

    if 'game_rounds' not in existing_tables:
        op.create_table('game_rounds',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('game_id', sa.Integer(), nullable=False),
            sa.Column('round_num', sa.Integer(), nullable=False),
            sa.Column('theme', sa.String(length=128), nullable=False),
            sa.Column('theme_description', sa.String(length=256), nullable=True),
            sa.Column('player1_image', sa.String(length=512), nullable=True),
            sa.Column('player2_image', sa.String(length=512), nullable=True),
            sa.Column('player1_uploaded_at', sa.DateTime(), nullable=True),
            sa.Column('player2_uploaded_at', sa.DateTime(), nullable=True),
            sa.Column('winner_id', sa.Integer(), nullable=True),
            sa.Column('is_tie', sa.Boolean(), nullable=False, server_default=sa.text('false')),
            sa.Column('ai_reasoning', sa.Text(), nullable=True),
            sa.Column('ai_feedback_p1', sa.Text(), nullable=True),
            sa.Column('ai_feedback_p2', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=32), nullable=False, server_default='uploading'),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['game_id'], ['games.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['winner_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'game_rounds' in existing_tables:
        op.drop_table('game_rounds')
    if 'games' in existing_tables:
        op.drop_table('games')

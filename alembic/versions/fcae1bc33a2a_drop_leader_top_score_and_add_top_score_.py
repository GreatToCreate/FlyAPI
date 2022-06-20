"""Drop leader, top_score, and add top_score_history table for changed historical tracking strategy

Revision ID: fcae1bc33a2a
Revises: 81daba9d219b
Create Date: 2022-06-20 13:21:49.920527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcae1bc33a2a'
down_revision = '81daba9d219b'
branch_labels = None
depends_on = None


# This reflects the change in historical tracking strategy. We're dropping top_score and leader as they're now drop and
# re-create tables handled by the analytics runners (done every t-minutes). top_score_history is now run once daily
# and is an append-only top 200 per course sink. We had to remove the definitions for the first 2 tables as alembic
# migrations would potentially fail based on the runner destroying/re-creating them. This deserves more
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('top_score_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('steam_id', sa.BigInteger(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('course', sa.String(length=40), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('leader')
    op.drop_table('top_score')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('top_score',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rank', sa.INTEGER(), nullable=True),
    sa.Column('steam_id', sa.BIGINT(), nullable=True),
    sa.Column('points', sa.INTEGER(), nullable=True),
    sa.Column('course', sa.VARCHAR(length=40), nullable=True),
    sa.Column('time', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leader',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('steam_id', sa.BIGINT(), nullable=True),
    sa.Column('steam_username', sa.VARCHAR(), nullable=True),
    sa.Column('points', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('top_score_history')
    # ### end Alembic commands ###

"""First Commit

Revision ID: 251c3fd09765
Revises: 
Create Date: 2021-12-03 20:07:54.553065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '251c3fd09765'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('snippets',
    sa.Column('snippet_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url_slug', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.Column('snippet', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('snippet_id', 'url_slug'),
    sa.UniqueConstraint('snippet_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('snippets')
    op.drop_table('users')
    # ### end Alembic commands ###

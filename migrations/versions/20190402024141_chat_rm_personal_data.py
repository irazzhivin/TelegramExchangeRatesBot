"""chat_rm_personal_data

Revision ID: 20190402024141
Revises: 20190328125146
Create Date: 2019-04-02 02:41:41.759954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20190402024141'
down_revision = '20190328125146'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'username')
    op.drop_column('chats', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('first_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('chats', sa.Column('username', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

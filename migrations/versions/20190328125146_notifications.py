"""notifications

Revision ID: 20190328125146
Revises: 20190326131313
Create Date: 2019-03-28 12:51:46.862444

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20190328125146'
down_revision = '20190326131313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('chat_id', sa.BigInteger(), nullable=False),
                    sa.Column('from_currency_id', sa.Integer(), nullable=False),
                    sa.Column('to_currency_id', sa.Integer(), nullable=False),
                    sa.Column('trigger_clause',
                              sa.Enum('more', 'less', 'diff', 'percent', name='notifytriggerclauseenum'),
                              nullable=False),
                    sa.Column('trigger_value', sa.Numeric(precision=24, scale=12), nullable=False),
                    sa.Column('last_rate', sa.Numeric(precision=24, scale=12), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('modified_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
                    sa.ForeignKeyConstraint(['from_currency_id'], ['currencies.id'], ),
                    sa.ForeignKeyConstraint(['to_currency_id'], ['currencies.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('chat_id', 'from_currency_id', 'to_currency_id')
                    )
    op.create_index(op.f('ix_notifications_is_active'), 'notifications', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notifications_is_active'), table_name='notifications')
    op.drop_table('notifications')
    # ### end Alembic commands ###
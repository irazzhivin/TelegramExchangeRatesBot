"""chat_settings

Revision ID: 20190314182214
Revises: 20190314175025
Create Date: 2019-03-14 18:22:14.635279

"""
import enum

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = '20190314182214'
down_revision = '20190314175025'
branch_labels = None
depends_on = None

Base = declarative_base()


class MoneyFormatEnum(enum.Enum):
    NO = None
    US = 'us'
    EU = 'eu'
    IN = 'in'
    RU = 'ru'


class CurrencyPositionEnum(enum.Enum):
    FROM = 'from'
    TO = 'to'


class Chat(Base):
    __tablename__ = 'chats'

    id = sa.Column(sa.BigInteger, primary_key=True)
    is_subscribed = sa.Column(sa.Boolean, default=True, nullable=False)
    is_console_mode = sa.Column(sa.Boolean, default=True, nullable=False)
    is_colored_arrows = sa.Column(sa.Boolean, default=True, nullable=False)
    money_format = sa.Column(sa.Enum(MoneyFormatEnum), default=MoneyFormatEnum.US.value, nullable=True)
    default_currency_id = sa.Column(sa.Integer, sa.ForeignKey('currencies.id'), nullable=False)
    default_currency_position = sa.Column(sa.Enum(CurrencyPositionEnum), default=CurrencyPositionEnum.TO.value, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, server_default=sa.func.now(), nullable=False)
    modified_at = sa.Column(sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)


class Currency(Base):
    __tablename__ = 'currencies'

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.Text, unique=True, nullable=False)


def upgrade():
    default_currency_position = postgresql.ENUM('from', 'to', name='default_currency_position')
    default_currency_position.create(op.get_bind())
    default_currency_position = postgresql.ENUM('us', 'eu', 'in', 'ru', name='money_format')
    default_currency_position.create(op.get_bind())

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('default_currency_id', sa.Integer(), nullable=True))
    op.add_column('chats', sa.Column('default_currency_position',
                                     sa.Enum('from', 'to', name='default_currency_position'), nullable=True))
    op.add_column('chats', sa.Column('is_colored_arrows', sa.Boolean(), nullable=True))
    op.add_column('chats', sa.Column('money_format', sa.Enum('us', 'eu', 'in', 'ru', name='money_format'),
                                     nullable=True))
    # ### end Alembic commands ###

    session = Session(bind=op.get_bind())
    default_currency = session.query(Currency).filter_by(code='USD').one()
    session.query(Chat).update({
        'default_currency_id': default_currency.id,
        'default_currency_position': CurrencyPositionEnum.TO.value,
        'is_colored_arrows': True,
        'money_format': MoneyFormatEnum.US.value,
        'modified_at': Chat.modified_at,
    })

    op.alter_column('chats', 'default_currency_id', nullable=False)
    op.alter_column('chats', 'default_currency_position', nullable=False)
    op.alter_column('chats', 'is_colored_arrows', nullable=False)
    op.create_foreign_key(None, 'chats', 'currencies', ['default_currency_id'], ['id'])


def downgrade():
    pass
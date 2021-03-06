"""add_btt_currency

Revision ID: 20190326060130
Revises: 20190324223003
Create Date: 2019-03-26 06:01:30.627169

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision = "20190326060130"
down_revision = "20190324223003"
branch_labels = None
depends_on = None

Base = declarative_base()


class Currency(Base):
    """
    https://en.wikipedia.org/wiki/ISO_4217

    See: migrations/versions/20190306193447_currencies_chat_request_foreigns.py
    """

    __tablename__ = "currencies"

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.Text, unique=True, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    is_active = sa.Column(sa.Boolean, index=True, nullable=False)
    is_crypto = sa.Column(sa.Boolean, index=True, nullable=False)


def upgrade():
    session = Session(bind=op.get_bind())
    session.add(Currency(code="BTT", name="BitTorrent", is_active=True, is_crypto=True))
    session.flush()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

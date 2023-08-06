import time

from sqlalchemy import Column, BigInteger, Integer, BLOB, UnicodeText

from packy_agent.domain_logic.models.sqlalchemy.base import ModelBase


class Measurement(ModelBase):
    __tablename__ = 'measurement'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True)
    measurement_type = Column(Integer, nullable=False)
    created_at_ts = Column(Integer, nullable=False, default=time.time)
    submitted_at_ts = Column(Integer)
    error_at_ts = Column(Integer)
    error_message = Column(UnicodeText)
    error_side = Column(Integer)
    value = Column(BLOB, nullable=False)

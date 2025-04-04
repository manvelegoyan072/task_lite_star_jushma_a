from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import BigInteger, String, DateTime, Column
from datetime import datetime


class User(BigIntAuditBase):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
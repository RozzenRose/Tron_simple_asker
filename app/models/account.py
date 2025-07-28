from app.database.engine import Base
from sqlalchemy import Column, Integer, BigInteger, String, Float


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_address = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    energy = Column(BigInteger, nullable=False)
    bandwidth = Column(BigInteger, nullable=False)

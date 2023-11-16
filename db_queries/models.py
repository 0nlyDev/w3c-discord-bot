from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'battle_tags'

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(50))
    battle_tag = Column(String(50+6))

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text, DateTime

from cog_nba.settings import ENGINE

from datetime import datetime

Base = declarative_base()


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True, autoincrement=True)
    endpoint = Column(Text)
    params = Column(Text)
    data = Column(Text)
    date = Column(DateTime, default=datetime.utcnow())


class DBConnection(object):

    def __init__(self):
        self.session = None

    def __enter__(self):
        Session = sessionmaker(bind=ENGINE)
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def create_tables():
    Base.metadata.create_all(ENGINE)

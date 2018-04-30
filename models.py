from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Inbound(Base):
    __tablename__ = 'inbound'
    status = Column(Integer, nullable=False)
    url = Column(String(250), primary_key=True)
    parents = Column(Text, nullable=False)


class Outbound(Base):
    __tablename__ = 'outbound'
    status = Column(Integer, nullable=False)
    url = Column(String(250), primary_key=True)
    parents = Column(Text, nullable=False)
    affiliates = relationship('Affiliate')


class Affiliate(Base):
    __tablename__ = 'affiliate'
    pk = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    url = Column(String(250), ForeignKey('outbound.url'))
    parents = Column(Text, nullable=False)


engine = create_engine('sqlite:///urls.db')
Base.metadata.create_all(engine)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Resource(Base):
    __tablename__ = 'resource'

    pk = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    domain = Column(String(8), nullable=False)  # inbound or outbound
    parent_url = Column(String(250), nullable=False)
    anchor_href = Column(String(250), nullable=False)
    redirect_url = Column(String(250))


class Affiliate(Base):
    __tablename__ = 'affiliate'

    pk = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    parent_url = Column(String(250), nullable=False)
    anchor_href = Column(String(250), nullable=False)
    redirect_url = Column(String(250))


engine = create_engine('sqlite:///urls.db')
Base.metadata.create_all(engine)

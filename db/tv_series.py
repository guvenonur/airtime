from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TvSeries(Base):
    __tablename__ = 'tv_series'

    imdb_id = Column('imdb_id', String(20), primary_key=True)
    name = Column('name', String(250), nullable=False, index=True)
    season = Column('season', Integer, nullable=True)
    episode = Column('episode', Integer, nullable=True)

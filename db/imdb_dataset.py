from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class ImdbDataset(Base):
    __tablename__ = 'imdb_dataset'

    imdb_id = Column('imdb_id', String(20), primary_key=True)
    primary_title = Column('primary_title', String(250), nullable=False, index=True)
    primary_title_lower = Column('primary_title_lower', String(250), nullable=False)


engine = create_engine('sqlite:///airtime.db')
Base.metadata.create_all(engine)
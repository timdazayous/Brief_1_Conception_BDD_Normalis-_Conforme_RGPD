from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class Genre(Base):
    __tablename__= 'Genres'
    id_genre = Column(Integer,primary_key=True)
    type_genre = Column(String, nullable=False)
    # relation avec Games
    games = relationship('Game', back_populates='genre')


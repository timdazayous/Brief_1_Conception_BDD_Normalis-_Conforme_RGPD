from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class Game_Platform(Base):
    __tablename__ = 'Games_Platforms'
    release_year = Column(Integer, nullable=True)
    # clés étrangères et primaires
    id_game = Column(Integer, ForeignKey('Games.id_game'), primary_key=True)
    id_platform = Column(Integer, ForeignKey('Platforms.id_platform'), primary_key=True)
    # relation avec les autres tables
    game = relationship('Game', back_populates='platforms_links')
    platform = relationship('Platform', back_populates='games_links')


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class User_Game(Base):
    __tablename__ = 'Users_Games'
    # clés étrangères et primaires
    id_user = Column(Integer, ForeignKey('Users.id_user'), primary_key=True)
    id_game = Column(Integer, ForeignKey('Games.id_game'), primary_key=True)
    # relation avec les autres tables
    # avec Games
    game = relationship('Game', back_populates='users_links')
    # avec Users
    user = relationship('User', back_populates='games_links')


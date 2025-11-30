from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class Game(Base):
    __tablename__ = 'Games'
    id_game = Column(Integer, primary_key=True)
    rank_game = Column(Integer)
    name_game = Column(String, nullable=False)
    # relation avec les autres tables
    # avec table de fait Sales
    sales = relationship('Sale', back_populates='game', cascade='all, delete-orphan')
    # avec table d'association Users_Games
    users_links = relationship('User_Game', back_populates='game', cascade='all, delete-orphan')
    # avec la table d'association Games_Platforms
    platforms_links = relationship('Game_Platform', back_populates='game', cascade='all, delete-orphan')
    # avec la table de dimensions Genres
    # clé etrangère venant de Genres
    id_genre_fk = Column(Integer, ForeignKey('Genres.id_genre'))
    genre = relationship('Genre', back_populates='games')
    # avec la table de dimensions Publishers
    # clé etrangère venant de Publishers
    id_publisher_fk = Column(Integer, ForeignKey('Publishers.id_publisher'))
    publishers = relationship('Publisher', back_populates='games')

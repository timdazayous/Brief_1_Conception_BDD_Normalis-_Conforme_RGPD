from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__= 'Users'
    # clé primaire
    id_user = Column(Integer, primary_key=True)
    pseudo_user = Column(String, nullable=False)
    password_user = Column(String,nullable=False)
    mail_user = Column(String,nullable=False, unique=True)
    consent_user = Column(bool,nullable=False)
    limitdate_user = Column(Integer, nullable=False)
    # relation avec les autres tables
    # avec table d'association Users_Games
    user_game = relationship('User_Game', back_populates='user')

class Game(Base):
    __tablename__ = 'Games'
    id_game = Column(Integer, primary_key=True)
    rank_game = Column(Integer)
    name_game = Column(String, nullable=False)
    # relation avec les autres tables
    # avec table de fait Sales
    game_sale = relationship('Sale', back_populates='game')
    # avec table d'association Users_Games
    user_game = relationship('User_Game', back_populates='game')
    # avec la table d'association Games_Platforms
    game_platform = relationship('Game_Platform', back_populates='game')
    # avec la table de dimensions Genres
    # clé etrangère venant de Genres
    id_genre_fk = Column(Integer, ForeignKey('Genres.id_genre'))
    game_genre = relationship('Genre', back_populates='game')
    # avec la table de dimensions Publishers
    # clé etrangère venant de Publishers
    id_publisher_fk = Column(Integer, ForeignKey('Publishers.id_publisher'))
    game_publisher = relationship('Publisher', back_populates='game')

## to be continued

class Sale(Base):
    __tablename__ = 'Sales'
    id_sale = Column(Integer, primary_key=True)
    NA_sale = Column(Integer, nullable=True)
    EU_sale= Column(Integer, nullable=True)
    JP_sale = Column(Integer, nullable=True)
    Other_sale = Column(Integer, nullable=True)
    Global_sale = Column(Integer, nullable=True)
    # relation avec les autres tables

class Publisher(Base):
    __tablename__= 'Publishers'
    id_publisher = Column(Integer, primary_key=True)
    name_publisher = Column(String, nullable=False)
    # relation avec les autres tables

class Platform(Base):
    __tablename__= 'Platforms'
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    # relation avec les autres tables

class Genre(Base):
    __tablename__= 'Genres'
    id_genre = Column(Integer,primary_key=True)
    type_genre = Column(String, nullable=False)
    # relation avec les autres tables

class User_Game(Base):
    __tablename__ = 'Users_Games'
    id_user_fk = Column(Integer, ForeignKey('Users.id_user'), primary_key=True)
    id_game_fk = Column(Integer, ForeignKey('Games.id_game'), primary_key=True)
    # relation avec les autres tables

class Game_Platform(Base):
    __tablename__ = 'Games_Platforms'
    release_year = Column(Integer, nullable=True)
    # relation avec les autres tables

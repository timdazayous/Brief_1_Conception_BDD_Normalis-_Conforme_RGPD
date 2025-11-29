from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__= 'Users'
    # clé primaire
    id_user = Column(Integer, primary_key=True)
    pseudo_user = Column(String, nullable=False)
    password_user = Column(String,nullable=False)
    mail_user = Column(String,nullable=False, unique=True) # à crypter
    consent_user = Column(bool,nullable=False)
    limitdate_user = Column(Integer, nullable=False)
    # relation avec les autres tables
    # avec table d'association Users_Games
    games = relationship('User_Game', back_populates='user')

class Game(Base):
    __tablename__ = 'Games'
    id_game = Column(Integer, primary_key=True)
    rank_game = Column(Integer)
    name_game = Column(String, nullable=False)
    # relation avec les autres tables
    # avec table de fait Sales
    sales = relationship('Sale', back_populates='game')
    # avec table d'association Users_Games
    users_games = relationship('User_Game', back_populates='game')
    # avec la table d'association Games_Platforms
    games_platforms = relationship('Game_Platform', back_populates='game')
    # avec la table de dimensions Genres
    # clé etrangère venant de Genres
    id_genre_fk = Column(Integer, ForeignKey('Genres.id_genre'))
    genres = relationship('Genre', back_populates='game')
    # avec la table de dimensions Publishers
    # clé etrangère venant de Publishers
    id_publisher_fk = Column(Integer, ForeignKey('Publishers.id_publisher'))
    publishers = relationship('Publisher', back_populates='game')

## to be continued

class Sale(Base):
    __tablename__ = 'Sales'
    id_sale = Column(Integer, primary_key=True)
    NA_sale = Column(Integer, nullable=True)
    EU_sale= Column(Integer, nullable=True)
    JP_sale = Column(Integer, nullable=True)
    Other_sale = Column(Integer, nullable=True)
    Global_sale = Column(Integer, nullable=True)
    # relation avec Games
    # clé etrangere 
    id_game_fk = Column(Integer, ForeignKey('Games.id_game'))
    games = relationship('Game', back_populates='sale')

class Publisher(Base):
    __tablename__= 'Publishers'
    id_publisher = Column(Integer, primary_key=True)
    name_publisher = Column(String, nullable=False)
    # relation avec Games
    games = relationship('Game', back_populates='publisher')

class Platform(Base):
    __tablename__= 'Platforms'
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    # relation avec Games_Plastforms
    games_platforms = relationship('Game_platform', back_populates='platform')

class Genre(Base):
    __tablename__= 'Genres'
    id_genre = Column(Integer,primary_key=True)
    type_genre = Column(String, nullable=False)
    # relation avec Games
    games = relationship('Game', back_populates='genre')

class User_Game(Base):
    __tablename__ = 'Users_Games'
    # clés étrangères et primaires
    id_user_pk_fk = Column(Integer, ForeignKey('Users.id_user'), primary_key=True)
    id_game_pk_fk = Column(Integer, ForeignKey('Games.id_game'), primary_key=True)
    # relation avec les autres tables
    # avec Games
    games = relationship('Game', back_populates='user_game')
    # avec Users
    users = relationship('User', back_populates='user_game')

class Game_Platform(Base):
    __tablename__ = 'Games_Platforms'
    release_year = Column(Integer, nullable=True)
    # clés étrangères et primaires
    id_game_pk_fk = Column(Integer, ForeignKey('Games.id_game'), primary_key=True)
    id_platform_pk_fk = Column(Integer, ForeignKey('Platforms.id_platform'), primary_key=True)
    # relation avec les autres tables
    games = relationship('Game', back_populates='game_platform')
    Platform = relationship('Platform', back_populates='game_platform')

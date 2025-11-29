from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# definition des tables de la BDD Games_Sales.db
class User(Base):
    __tablename__= 'Users'
    # clé primaire
    id_user = Column(Integer, primary_key=True)
    pseudo_user = Column(String, nullable=False)
    password_user = Column(String,nullable=False)
    mail_user = Column(String,nullable=False)
    consent_user = Column(bool,nullable=False)
    limitdate_user = Column(Integer, nullable=False)

    # relation 0,n un User peut avoir plusieurs Games entre Games et Users User_Game
    user_has_games = relationship('Game_User', back_populates="user", cascade="all, delete-orphan")

    # games = realtionship('Game', secondary='user_has_games', viewonly=True)

class Game(Base):
    __tablename__ = 'Games'
    id_game = Column(Integer, primary_key=True)
    rank_game = Column(Integer)
    name_game = Column(String, nullable=False)
    # clé etrangere de Publishers et Genres
    id_publisher_fk = Column(Integer, ForeignKey('Publishers.id_publisher'), nullable=False)
    id_genre_fk = Column(Integer, ForeignKey('Genres.id_genre'), nullable=False)
    # relations avec les autres tables
    # avec table de fait Sales
    game_sale = relationship('Sale',back_populates='game')
    # avec les tables de dimensions Publishers et Genres
    publisher_game = relationship()
    # avec les differentes tables d'association possède Game_Platform et détient User_Game
    user_has_games = relationship('User_Game', back_populates="game")
    game_has_platform = relationship('Game_Platform', back_populates='game')
    

# table de fait Sales
class Sale(Base):
    __tablename__ = 'Sales'
    id_sale = Column(Integer, primary_key=True)
    NA_sale = Column(Integer, nullable=True)
    EU_sale= Column(Integer, nullable=True)
    JP_sale = Column(Integer, nullable=True)
    Other_sale = Column(Integer, nullable=True)
    Global_sale = Column(Integer, nullable=True)
    # clé étangère venant de Games
    id_game_fk = Column(Integer, ForeignKey('Games.id_game'), nullable=False)
    # relation avec Games
    game_sale = relationship('Game', back_populates='sale')

class Publisher(Base):
    __tablename__= 'Publishers'
    id_publisher = Column(Integer, primary_key=True)
    name_publisher = Column(String)

    games_publishers = relationship('Game', back_populates='publisher')

class Platform(Base):
    __tablename__= 'Platforms'
    id = Column(Integer,primary_key=True)
    name = Column(String)

class Genre(Base):
    __tablename__= 'Genres'
    id_genre = Column(Integer,primary_key=True)
    type_genre = Column(String)

# classe d'association detient entre Users et Games
class Game_User(Base):
    __tablename__= 'users_games'
    id = Column(Integer, primary_key=True)
    id_user_fk = Column(Integer, ForeignKey('Users.id'), primary_key='')
    Users = relationship('Users', back_populate='detient')
    id_game_fk = Column(Integer, ForeignKey('Games.id'))
    Games = relationship('Games', back_populates='detient')

# classe d'association possède entre Platforms et Games
class Game_Platform(Base):
    __tablename__ = 'Platforms_Games'
    release_year = Column(Integer,nullable=True)


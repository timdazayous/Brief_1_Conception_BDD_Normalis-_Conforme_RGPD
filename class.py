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
    mail_user = Column(String,nullable=True)
    consent_user = Column(bool,nullable=False)
    limitdate_user = Column(Integer, nullable=True)

    # relation 0,n un User peut avoir plusieurs Games entre Games et Users User_Game
    user_has_games = relationship('Game_User', back_populates="user", cascade="all, delete-orphan")

    # games = realtionship('Game', secondary='user_has_games', viewonly=True)

class Game(Base):
    __tablename__ = 'Games'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    # relations avec les autres tables
    # avec table de fait Sales
    sales = relationship('Sale',back_populates='game')
    # avec les differentes tables d'association
    user_has_games = relationship('User_Game', back_populates="game")
    game_has_publisher = relationship('Publisher_Game', back_populates='game')
    game_has_platform = relationship('Game_Platform', back_populates='game')
    game_has_genre = relationship('Game_Genre')

# table de fait Sales
class Sale(Base):
    __tablename__ = 'Sales'
    id = Column(Integer, primary_key=True)
    NA = Column(Integer)
    EU = Column(Integer)
    JP = Column(Integer)
    Other = Column(Integer)
    Global = Column(Integer)
    # clé étangère venant de Games
    id_game_fk = Column(Integer, ForeignKey('Games.id'))
    # relation avec Games
    games = relationship('Game', back_populates='sale')

class Publisher(Base):
    __tablename__= 'Publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    game_has_publisher = relationship('Game_Publisher', back_populates='publisher')

class Platform(Base):
    __tablename__= 'Platforms'
    id = Column(Integer,primary_key=True)
    name = Column(String)

class Genre(Base):
    __tablename__= 'Genres'
    id = Column(Integer,primary_key=True)
    type = Column(String)

# classe d'association detient entre Users et Games
class Game_User(Base):
    __tablename__= 'users_games'
    id = Column(Integer, primary_key=True)
    id_user_fk = Column(Integer, ForeignKey('Users.id'))
    Users = relationship('Users', back_populate='detient')
    id_game_fk = Column(Integer, ForeignKey('Games.id'))
    Games = relationship('Games', back_populates='detient')

# classe d'association publie entre Publishers et Game
class Game_Publisher(Base):
    __tablename__ = 'Games_Publishers'
    id = Column(Integer,primary_key=True)
    id_game_fk = Column(Integer,ForeignKey('Games.id'))
    Games = relationship('Games', back_populates='publie')
    id_publisher_fk = Column(Integer,ForeignKey('Games.id'))
    Publishers = relationship('Publisher', back_populates='publie')

# classe d'association possède entre Platforms et Games
class Game_Platform(Base):
    __tablename__ = 'Platforms_Games'
    release_year = Column(Integer,nullable=True)

# classe d'association présente entre Genres et Games
class Game_Genre(Base):
    __tablename__ = 'Games_Genres'

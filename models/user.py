from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class User(Base):
    __tablename__= 'Users'
    # clé primaire
    id_user = Column(Integer, primary_key=True)
    pseudo_user = Column(String, nullable=False)
    password_user = Column(String,nullable=False)
    mail_user = Column(String,nullable=False, unique=True) # à crypter
    consent_user = Column(Boolean,nullable=False)
    limitdate_user = Column(Integer, nullable=False)
    # relation avec les autres tables
    # avec table d'association Users_Games
    games_links = relationship('User_Game', back_populates='user')
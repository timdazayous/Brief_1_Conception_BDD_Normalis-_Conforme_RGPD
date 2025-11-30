from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class Platform(Base):
    __tablename__= 'Platforms'
    id_platform = Column(Integer,primary_key=True)
    name_platform = Column(String, nullable=False)
    # relation avec Games_Plastforms
    games_links = relationship('Game_Platform', back_populates='platform')
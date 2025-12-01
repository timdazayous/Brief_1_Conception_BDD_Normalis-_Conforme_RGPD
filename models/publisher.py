from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

class Publisher(Base):
    __tablename__= 'Publishers'
    id_publisher = Column(Integer, primary_key=True)
    name_publisher = Column(String, nullable=True)
    # relation 1,n avec Games 
    games = relationship('Game', back_populates='publishers')
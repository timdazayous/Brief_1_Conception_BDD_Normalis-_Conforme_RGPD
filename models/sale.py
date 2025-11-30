from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship # ,declarative_base
# On recupere base depuis database.py
from database import Base
# Base = declarative_base()

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
    id_game_fk = Column(Integer, ForeignKey('Games.id_game'), nullable=False)
    game = relationship('Game', back_populates='sales')
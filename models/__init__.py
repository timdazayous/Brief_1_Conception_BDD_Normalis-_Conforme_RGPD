from database import Base, engine
from models.class import class as models

Base.metadata.create_all(engine)
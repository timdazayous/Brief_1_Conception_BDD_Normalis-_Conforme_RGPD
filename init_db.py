from database import Base, engine, DATABASE_URL
import models

Base.metadata.create_all(bind=engine)

print(f'Base de données :{DATABASE_URL} initialisée')
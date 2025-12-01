from database import Base, engine, DATABASE_URL
import models

Base.metadata.create_all(bind=engine)

db_path = DATABASE_URL.replace("sqlite:///", "")
db_name = os.path.basename(db_path)
print(f'Base de données :{db_path} initialisée')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Connexion à une base de données SQLite :
# L'argument 'sqlite:///ma_base_clients.db' crée un fichier 'ma_base_clients.db' 
# dans le répertoire courant s'il n'existe pas.
DATABASE_URL = "sqlite:///Games_Sales.db"
engine = create_engine(DATABASE_URL, echo=True)

# 2. Création des tables dans la base de données
# Cette ligne regarde toutes les classes qui héritent de Base (Client, Commande) 
# et crée les tables SQL correspondantes (si elles n'existent pas déjà).
Base = declarative_base()
# Base.metadata.create_all(engine) # Dans __init__.py 

# 3. Configuration de la session :
# Lie la session à notre moteur (engine) pour pouvoir interagir avec la BDD.
# Session = sessionmaker(bind=engine) # dans le main.py

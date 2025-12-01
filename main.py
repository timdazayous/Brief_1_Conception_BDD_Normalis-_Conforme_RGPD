from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models

def main():
    # ouverture d'une nouvelle session
    session = Session()

    # bloc try execpt pour recuperer les erreurs lors de lexecution du main
    try:
        while True:
        print("\n1. Créer un user")
        print("2. Lire un user")
        print("3. Modifier un user")
        print("4. Supprimer un user")
        print("0. Quitter")
        choix = input("Choix : ")

    except:


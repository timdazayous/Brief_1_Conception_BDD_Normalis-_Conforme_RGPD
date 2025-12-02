from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models
from services.user_services import create_user, read_user, delete_user, update_user

def main():
    # ouverture d'une nouvelle session
    session = Session()

    # bloc try execpt pour recuperer les erreurs lors de lexecution du main
    try:
        while True:
            print("1. Créer un user")
            print("2. Lire un user")
            print("3. Modifier un user")
            print("4. Supprimer un user")
            print("5. Quitter")
            choix = input("Choix : ").strip()

            if choix == "1":
                create_user(session)
            elif choix == '2':
                read_user()
            elif choix == '3':
                update_user()
            elif choix == '4':
                delete_user()
            elif choix == '5':
                print('fin')
                break
            else:
                print('Choix invalide, réessayez')
    except SQLAlchemyError as e:
        print(f"Erreur SQLAlchemy dans le programme : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()


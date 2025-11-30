# main.py
from database import Session
import models

def main():
    session = Session()
    try:
        # Exemple : créer un utilisateur
        new_user = models.User(
            pseudo_user="toto",
            password_user="secret",
            mail_user="toto@example.com",
            consent_user=True,
            limitdate_user=20251231,
        )
        session.add(new_user)
        session.commit()

        # Lire et afficher les utilisateurs
        users = session.query(models.User).all()
        for u in users:
            print(u.id_user, u.pseudo_user)

    finally:
        session.close()

if __name__ == "__main__":
    main()

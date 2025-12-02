import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models
import bcrypt


# liste des localités possible pour diversifier les utilisateurs et etre un peu plus representatif de la realité 
LOCALES = ['fr_FR', "en_US", "ja_JP", "de_DE", "es_ES", "it_IT", "pt_BR"]

# fonction pour hasher un mdp 
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')



def generate_fake_user():
    locale = random.choice(LOCALES)
    fake = Faker(locale)

    pwd = fake.password(length=10)
    hashed_pwd = hash_password(pwd)

    return {
        "pseudo_user": fake.user_name(),
        "password_user": hashed_pwd,
        "mail_user": fake.unique.email(),
        "consent_user": fake.boolean(chance_of_getting_true=85), # taux d'acceptation du consentement ici 85%
        "limitdate_user": int(fake.date_between(start_date='+1y', end_date='+3y').strftime("%Y%m%d")) # genere une date limite entre +1 an et +3 ans aleatoirement
    }

# ajout de fake users avec des liens randomisés avec Game
def create_users_and_links(nb_users=50, max_games_per_user=5): # par défaut 50 joueurs possédant de 0 a 5 jeux
    session = Session()
    try:
        # on recupere tous les jeux depuis la class Game
        all_games = session.query(models.Game).all()
        # on verifie qu'il y a bien des jeux dans la base de données
        if not all_games:
            print('Pas de jeux enregistrés') # apres chargment du csv on ne devrait jamais avoir ce probleme
            return
        
        # on va tracker le nb de users associés a des jeux pour pouvoir afficher quelques details lors de la generation des faux utilisateurs
        users_with_links = 0

        for i in range(nb_users):
            user_data = generate_fake_user()
            user = models.User(**user_data)
            session.add(user)
            session.flush()

            # on attribut aleatoirement le nombre de jeux de l'utilisateur
            nb_jeux = random.randint(0, max_games_per_user)

            if nb_jeux > 0:
                jeux_choisis = random.sample(all_games, k=min(nb_jeux, len(all_games)))

                # création des liens entre User et Game
                for game in jeux_choisis:
                    link = models.User_Game(id_user=user.id_user, id_game=game.id_game) # On créer les fk id_game et if_user dans Game_User
                    session.add(link)
                users_with_links += 1 # ajout d'un joueur avec au moins 1 jeu
                print(f'Utilisateur : {user.pseudo_user} lié à {nb_jeux} jeu(x)')
            else:
                print(f"Utilisateur {user.pseudo_user} n'est lié à aucun jeu")

        session.commit()
        print(f'{nb_users} utilisateur(s) créé(s) avec Faker')
        print(f'{users_with_links} utilisateurs ont au moins 1 jeu ')
        print(f"{nb_users - users_with_links} n'ont aucun jeu")
    except SQLAlchemyError as e:
        session.rollback()
        print(f'Erreur lors de la création des utilisateurs et ou des liens avec Faker: {e}')
    finally:
        session.close()

if __name__ == '__main__':
    create_users_and_links()

# 50 utilisateur(s) créé(s) avec Faker
# 42 utilisateurs ont au moins 1 jeu 
# 8 n'ont aucun jeu
        
# 50 utilisateur(s) créé(s) avec Faker
# 36 utilisateurs ont au moins 1 jeu 
# 14 n'ont aucun jeu
# mdp hashé
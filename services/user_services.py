from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models

def input_user_data():
    pseudo_user = input('Pseudo: ')
    password_user = input('Mot de passe: ')        
    mail_user = input('Mail: ')
    consent = input('Consentement (oui / non, yes / no): ')
    #consent = consent.lower()
    #if consent == 'oui' or consent =='yes':
    #    consent_user = True
    #else:
    #    consent_user = False
    # regarde si consent est egale a oui ou yes et en fonction retourne true ou false dans consent_user
    consent_user = consent.lower() in ('oui', 'yes')
    limitdate = input('Date limite utilisation de données(AAAAMMJJ): ')
    try:
        limitdate_user = int(limitdate)
    except ValueError:
        limitdate_user = 0

    return { 
        "pseudo_user": pseudo_user,
        "password_user": password_user,
        "mail_user": mail_user,
        "consent_user": consent_user,
        "limitdate_user": limitdate_user
    }

def create_user(session):
    data = input_user_data()
    try:
        user = models.User(**data)
        session.add(user)
        session.flush()
        
        # user ayant des jeux ?
        all_games = session.query(models.Game).all()
        if all_games:
            print("Choississez le ou les ID(s) des jeux que vous souhaitez ajouter au nouvel utilisateur")
            for game in all_games: 
                print(f'ID {game.id_game} - {game.name_game}')

            choix = input('ID(s) séparés par une virgule ou vide si pas de jeu:').strip()

            if choix:
                ids = [int(x) for x in choix.split(',') if x.strip().isdigit()]
                #nb_jeux_lies = 0

                for game_id in ids:
                    if any(g.id_game == game_id for g in all_games):
                        link = models.User_Game(id_user = user.id_user, id_game = game_id)
                        session.add(link)
                        #nb_jeux_lies += 1
                    else:
                        print(f"Jeu ID {game_id} n'existe pas")

                    #print(f'{nb_jeux_lies} Jeu(x) lié(s) ')
            session.commit()
        # user.games_links contient la liste des objets User_Game reliant user a jeux donc en recuperant sa length on a le nombre de jeux liés ne fonctionne pas avant de commit 
        print(f'User {user.pseudo_user} créé avec {len(user.games_links)} jeu(x) lié(s)')

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'ajout du nouvel user: {e}")

def read_user():
    session = Session()
    try:
        # Affichages possibles:
        # tous les Users
        # users avec au moins 1 jeu
        # users liés à un jeu precis
        # user par ID
        # user par pseudo
        print("\n=== Options d'affichage des Users ===")
        print("1. Afficher tous les users")
        print("2. Afficher les users avec au moins un jeu")
        print("3. Afficher les users liés à un jeu précis")
        print("4. Afficher un user par ID")
        print("5. Afficher un user par pseudo")
        choix = input("Choix (1-5) : ").strip()

        if choix == '1':
            # requete
            users = session.query(models.User).all()
            print(f'Liste des {len(users)} user(s)')
            for u in users:
                print(f'ID {u.id_user} - {u.pseudo_user} - nombre de jeu(x): {len(u.games_links)}')
        elif choix =='2':
            # requete
            users = session.query(models.User).join(models.User_Game).distinct().all()
            print(f'Liste des {len(users)} users ayant au moins un jeu')
            for u in users:
                print(f'ID {u.id_user} - {u.pseudo_user} - nombre de jeu(x): {len(u.games_links)} ')
        elif choix == '3':
            # requete
            all_games = session.query(models.Game).all()
            if not all_games:
                print('Aucun jeu dans la base de données')
                return
            print('Liste des jeux: ')
            for game in all_games:
                print(f'ID {game.id_game} - {game.name_game}')
            linked_game_str = input("Entrez l'ID du jeu: ").strip
            if not linked_game_str.isdigit():
                print('ID invalide')
                return
            linked_game_id = int(linked_game_str)

            # requete
            users = session.query(models.User).join(models.User_Game).filter(models.User_Game.id_game == linked_game_id).all()
            linked_game = session.get(models.Game, linked_game_id)
            linked_game_name = linked_game.name_game if linked_game else 'jeu inconnu'
            print(f'{len(users)} user(s) lié(s) au jeu ID: {linked_game_id} - {linked_game_name}')
            for u in users:
                print(f"ID {u.id_user} | {u.pseudo_user}")
        
        elif choix =='4':
            user_id_str = input("Entrez l'ID de l'User recherché").strip()
            if not user_id_str.isdigit():
                print('ID invalide')
                return
            user_id = int(user_id_str)
            user = session.get(models.User, user_id)
            if not user:
                print('User non trouvé')
                return
            print(f'ID {user.id_user} - {user.pseudo_user} - lié à {len(user.games_links)} jeu(x)')
            # affichage de la liste des jeux associés en suivant pour eviter la redondance du nom user et de l'id user 
            for link in user.games_links:
                print(f'{link.game.name_game}')
        # a relire la suite        
        elif choix == "5":
            pseudo = input("Entrez le pseudo complet ou partiel : ").strip()
            users = session.query(models.User).filter(models.User.pseudo_user.ilike(f"%{pseudo}%")).all()
            print(f"\nUsers avec pseudo contenant '{pseudo}' ({len(users)}):")
            for u in users:
                print(f"ID {u.id_user} | {u.pseudo_user} | Jeux liés: {len(u.games_links)}")

        else:
            print("Choix invalide.")

    except Exception as e:
        print(f"Erreur lors de la lecture des users : {e}")
    finally:
        session.close()

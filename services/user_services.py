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

# create
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

# select
def read_user():
    session = Session()
    try:
        # Affichages possibles:
        # tous les Users
        # users avec au moins 1 jeu
        # users liés à un jeu precis
        # user par ID
        # user par pseudo
        print("=== Options d'affichage des Users ===")
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
            linked_game_str = input("Entrez l'ID du jeu: ").strip()
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
                print(f"ID {u.id_user} - {u.pseudo_user}")
        
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
        elif choix == "5":
            pseudo = input("Entrez le pseudo exact : ").strip()
            users = session.query(models.User).filter(models.User.pseudo_user == pseudo).all()
    
            if users:
                print(f"\n{len(users)} user(s) avec le pseudo '{pseudo}' :")
                for u in users:
                    print(f"  ID {u.id_user} - {u.pseudo_user} - Jeux liés : {len(u.games_links)}")
                    # lister les jeux pour chaque user
                    if u.games_links:
                        for link in u.games_links:
                            print(f"    - {link.game.name_game}")
            else:
                print(f"Aucun user avec le pseudo '{pseudo}'.")

        else:
            print("Choix invalide.")

    except Exception as e:
        print(f"Erreur lors de la lecture des users : {e}")
    finally:
        session.close()

# Update
def update_user():
    session = Session()
    try:
        user_id_str = input("Saisissez l'ID de l'user à modifier: ").strip()
        if not user_id_str.isdigit():
            print('ID invalide')
            return
        
        user_id = int(user_id_str)
        user = session.get(models.User, user_id)
        if not user:
            print('user non trouvé')
            return
        
        print(f"User actuel : ID {user.id_user} - {user.pseudo_user}")
        print(f"Email : {user.mail_user} - Consentement : {user.consent_user}")
        print(f"Date limite : {user.limitdate_user}")
        print(f"Jeux liés ({len(user.games_links)}) :")
        if user.games_links:
            for link in user.games_links:
                print(link.game.name_game)
        else:
            print("aucun jeu lié a l'user")

        print('Appuyez sur entrée pour laisser inchangé')

        # Saisie des nouveaux champs
        nouveau_pseudo = input('Saisissez le nouveau pseudo: ').strip()
        nouveau_mail = input("Nouvel email : ").strip()
        nouveau_consent_str = input("Nouveau consentement (oui / yes non / no) : ").strip()
        nouveau_limitdate_str = input("Nouvelle date limite (AAAAMMJJ) : ").strip()

        updates = False
        if nouveau_pseudo:
            user.pseudo_user = nouveau_pseudo
            updates = True
        if nouveau_mail:
            user.mail_user = nouveau_mail
            updates = True
        if nouveau_consent_str:
            val = nouveau_consent_str.lower()
            if val in ('oui', 'yes'):
                user.consent_user = True
                updates = True
            elif val in ('non', 'no'):
                user.consent_user = False
                updates = True
            else:
                print("Réponse consentement non reconnue, laissé inchangé.")
        if nouveau_limitdate_str:
            try:
                user.limitdate_user = int(nouveau_limitdate_str)
                updates = True
            except ValueError:
                print('Date invalide, valeur ignorée.')

        # Gestion des liens jeux dans une boucle interactive
        while True:
            print("--- Gestion des jeux ---")
            print("1. Ajouter un jeu (ID)")
            print("2. Supprimer un jeu (ID)")
            print("3. Terminer")
            choix_jeux = input("Choix (1-3) : ").strip()

            if choix_jeux == "1":
                # Ajouter un jeu par ID
                while True:
                    jeu_id_str = input("ID du jeu à ajouter (0 pour annuler) : ").strip()
                    if jeu_id_str == "0":
                        break
                    try:
                        game_id = int(jeu_id_str)
                        game = session.get(models.Game, game_id)
                        if game:
                            if not any(link.id_game == game_id for link in user.games_links):
                                lien = models.User_Game(id_user=user.id_user, id_game=game_id)
                                session.add(lien)
                                print(f"{game.name_game} (ID {game_id}) ajouté !")
                            else:
                                print(f"ID {game_id} déjà lié.")
                        else:
                            print(f"Jeu ID {game_id} n'existe pas.")
                    except ValueError:
                        print("ID invalide.")

            elif choix_jeux == "2":
                # Supprimer un jeu par ID
                if not user.games_links:
                    print("Aucun jeu à supprimer.")
                    continue
                
                print("\nJeux actuels :")
                for link in user.games_links:
                    print(f"  ID {link.id_game} - {link.game.name_game}")
                
                while True:
                    jeu_id_str = input("ID du jeu à supprimer (0 pour annuler) : ").strip()
                    if jeu_id_str == "0":
                        break
                    try:
                        game_id = int(jeu_id_str)
                        lien = session.query(models.User_Game).filter_by(id_user=user.id_user, id_game=game_id).first()
                        if lien:
                            session.delete(lien)
                            print(f" Jeu ID {game_id} supprimé !")
                        else:
                            print(f" Lien ID {game_id} non trouvé.")
                    except ValueError:
                        print(" ID invalide.")

            elif choix_jeux == "3":
                break  
            else:
                print("Choix invalide, réessayez.")

        # Commit final s'il y a eu des mises à jour ou des changements sur les liens
        if updates:
            session.commit()
            print(f"Modifications sauvegardées pour l'user {user.pseudo_user} !")
        else:
            session.commit()  # pour enregistrer ajouts/suppressions de liens
            print(f"Changements sur jeux sauvegardés pour {user.pseudo_user}.")

        print(f"User {user.pseudo_user} a maintenant {len(user.games_links)} jeu(x) lié(s)")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de la mise à jour : {e}")
    finally:
        session.close()

# delete
def delete_user():
    session = Session()
    try:
        user_id_str = input("Entrez l'ID de l'utilisateur à supprimer:").strip()
        if not user_id_str.isdigit():
            print('ID invalide')
            return
        
        user_id = int(user_id_str)
        user = session.get(models.User, user_id)
        if not user:
            print('Utilisateur non trouvé')
            return
        
        # demande de confirmation de la suppression
        confirm = input(f"Confirmez-vous la suppression de l'utilisateur {user.pseudo_user} - ID {user_id} ? (oui/non yes/no)").strip().lower()
        if confirm not in ('oui', 'yes'):
            print('suppression annulée')
            return
        
        session.delete(user)
        session.commit()
        # affichage de confirmation de suppression
        print(f"Utilisateur {user.pseudo_user} - {user_id} suprimé")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de la suppression de l'utilisateur: {e}")
    finally: 
        session.close()

    
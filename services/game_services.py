from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models

def input_game_data(session):
    # nom
    name_game = input('Nom du jeu: ')
    # rank
    while True:
        rank_str = input('Rank du jeu (entier): ').strip()
        try:
            rank_game = int(rank_str)
            break # sortie si la conversion se deroule bien uniquement
        except ValueError:
            print('Rank invalide, entier seulement')
    # genre
    genres = session.query(models.Genre).all()
    # verification que Genres nest pas vide
    if not genres:
        print('Aucun genre disponible')
        id_genre = None
    else:
        # affichage de la liste des genres
        print('Genres disponibles: ')
        for g in genres:
            print(f"ID {g.id_genre} - {g.name_genre}")
        while True:
            genre_str = input('ID du genre (entrée pour passer)').strip()
            if genre_str == "":
                id_genre = None
                break # sortie validée
            if not genre_str.isdigit():
                print('ID invalide, saisissez un nombre ou laisser vide')
                continue # on reboucle

            genre_temp = int(genre_str)
            if any(g.id_genre == genre_temp for g in genres):
                id_genre = genre_temp
                break # sortie validée
            else:
                print('ID invalide, inexistant')
    # publisher
    publishers = session.query(models.Publisher).all()
    id_publisher = None

    if not publishers:
        print('Aucun publisher renseigné dans la base') # id_publisher reste donc none
    else:
        print('Publishers disponibles: ')
        # affichage de la liste des publishers
        for p in publishers:
            print(f"ID {p.id_publisher} - {p.name_publisher}")

    while True:
        pub_str = input("Saisissez l'id du publisher (entrée pour passer)").strip()
        if pub_str =='':
            break

        if not pub_str.isdigit():
            print('ID invalide (entier ou vide)')
            continue
        pub_temp = int(pub_str)
        if any(p.id_publisher == pub_temp for p in publishers):
            id_publisher = pub_temp
            break
        else:
            print('ID inexistant')

    return {
        "rank_game": rank_game,
        "name_game": name_game,
        "id_genre_fk": id_genre,
        "id_publisher_fk": id_publisher
    }

# Create
def create_game():
    session = Session()
    try:
        data = input_game_data(session)
        game = models.Game(**data)
        session.add(game)
        session.commit()
        print(f'Jeu {game.name_game} ID {game.id_game} créé ')
    except SQLAlchemyError as e:
        session.rollback()
        print((f'Erreur lors de la creation du jeu: {e}'))
    finally:
        session.clos()

# Read
def read_game():
    session = Session()
    try:
        print("=== Options d'affichage des Jeux ===")
        print("1. Tous les jeux")
        print("2. Jeu par ID")
        print("3. Jeux par nom (contient)")
        choix = input("Choix (1-3) : ").strip()

        if choix =='1':
            games = session.query(models.Game).all()
            # affichage de tous les jeux
            print(f'Affichage de {len(games)} jeu(x)')
            for g in games:
                genre = g.genre.name_genre if g.genre else "N/A"
                pub = g.publisher.name_publisher if g.publisher else "N/A"
                print(f"ID {g.id_game} - Rank {g.rank_game} - Name {g.name_game} - Genre {genre} - Publisher {pub}")

        elif choix =='2':
            game_id_str = input('ID du jeu: ').strip()
            if not game_id_str.isdigit():
                print('ID invalide')
                return
            game = session.get(models.Game, int(game_id_str))
            if not game:
                print('ID du jeu non trouvée')
                return
            genre = game.genre.name_genre if game.genre else 'N/A'
            pub = game.publisher.name_publisher if game.publisher else 'N/A'
            print(f'ID {game.id_game} - Rank {game.rank_game} - Name {game.name_game} - Genre {genre} - Publisher {pub}')
        
        elif choix == '3':
            # Nom du jeu ou nom proche pour la recherche recherche plus permissive 
            name = input('Nom du jeu: ')
            games = session.query(models.Game).filter(models.Game.name_game.ilike(f"%{name}%")).all()
            print(f'{len(games)} jeu(x) trouvé(s): ')
            for g in games:
                print(f'ID {g.id_game} - {g.name_game}')
        else:
            print('choix invalide')
    except Exception as e:
        print(f'Erreur lors de la lecteur des jeux: {e}')
    finally:
        session.close()

# Update
def update_game():
    session = Session()
    try: 
        game_id_str = input('ID du jeu à modifier: ').strip()
        if not game_id_str.isdigit():
            print('ID invalide')
            return
        game = session.gets(models.Game, int(game_id_str))
        if not game:
            print('jeu non trouvé')
            return
        # jeu trouvé
        print(f"Jeu trouvé: ID {game.id_game} - Rank {game.rank_game}- {game.name_gmae}")

        # demande de saisi des modifications
        new_rank_str = input('Nouveau rank (entier / entrée pour passer ou valider)').strip()
        new_name = input ('Nouveau nom (entrée pour passer ou valider)').strip()
        # modification du genre
        genres = session.query(models.Genre).all()
        id_genre = game.id_genre_fk
        print("Saisissez le nouveau genre (entrée pour passer ou valider)")
        # affichage de la liste des genres disponibles
        if genres:
            print('Liste du ou des genres disponibles')
            for g in genres:
                print(f'ID {g.id_genre} - {g.type_genre}')
            genre_str = input('Nouvel ID genre (entrée pour passer / 0 pour enlever le genre actuel): ').strip()
            if genre_str == '0':
                id_genre = None
            elif genre_str and genre_str.isdigit():
                genre_id = int(genre_str)
                if any(g.id_genre == genre_id for g in genres):
                    id_genre = genre_id
                else:
                    print('ID genre invalide, inchangé, genre non trouvé')
        # modification de Publisher
        publishers = session.query(models.Publisher).all()
        id_publisher = game.id_publisher_fk
        print('Saisissez le nouveau publisher (entrée pour passer ou valider)')
        if publishers:
            print('Liste des publishers disponibles')
            for p in publishers:
                print(f"ID {p.id_publisher} - {p.name_publisher}")
            publisher_str = input('Nouvel ID publisher (entrée pour passer / 0 pour enlever le publisher actuel)').strip()
            if publisher_str == '0':
                id_publisher = None
            elif publisher_str and publisher_str.isdigit():
                publisher_id = int(publisher_str)
                if any (p.id_publisher == publisher_id for p in publishers):
                    id_publisher = publisher_id
                else:
                    print('ID invalide, inchangé, publisher non trouvé')
        # mise en place des modifications
        updated = False
        if new_rank_str:
            try:
                game.rank_game = int(new_rank_str)
                updated = True
            except ValueError:
                print('Rank Invalide, non modifié')
        if new_name:
            game.name_game = new_name
            updated = True
        if id_genre != game.id_genre_fk:
            game.id_genre_fk = id_genre
            updated = True
        if id_publisher != game.id_publisher_fk:
            game.id_publisher_fk = id_publisher
            updated = True

        # si modification effectuées on commit
        if updated:
            session.commit()
            print('Jeu mis à jour')
        else:
            print('Aucun changement effectué')

    except SQLAlchemyError as e:
        print(f'Update du jeu impossible: {e}')
    finally:
        session.close()

# Delete
def delete_game():
    session=Session()
    try:
        game_id_str = input('ID du jeu à supprimer: ').strip()
        if not game_id_str.isdigit():
            print('ID invalide')
            return
        game = session.get(models.Game, int(game_id_str))
        if not game:
            print('ID invalide, jeu non trouvé')
            return
        confirm = input(f'Confirmer la suppression du jeu ID {game.id_game} - {game.name_game}? (oui/non, yes/no)').strip().lower()
        if confirm not in ('oui', 'yes'):
            print('Suppresion annulée')
            return
        # suppression du jeu 
        session.delete(game)
        session.commit()
        print('Jeu supprimé')
    except SQLAlchemyError as e:
        print(f'Erreur lors de la suppresion du jeu: {e}')
    finally:
        session.close()
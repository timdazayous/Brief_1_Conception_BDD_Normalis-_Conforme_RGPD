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
    publishers = session.query(models.Publisher).all
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
        print(('Erreur lors de la creation du jeu: {e}'))
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
                print('ID {g.id_game} - {g.name_game}')
        else:
            print('choix invalide')
    except Exception as e:
        print(f'Erreur lors de la lecteur des jeux: {e}')
    finally:
        session.close()


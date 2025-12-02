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
            if any(g.id_genre == genre_temp for g in genres)
                id_genre = genre_temp
                break # sortie validée
            else:
                print('ID invalide, inexistant')
    # publisher
    publishers = session.query(models.Publisher)
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
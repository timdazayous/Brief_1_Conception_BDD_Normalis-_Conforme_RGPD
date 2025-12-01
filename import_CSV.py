import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models

CSV_path = 'vgsales.csv'

def populate_from_CSV(CSV_path):
    CSV_df = pd.read_csv(CSV_path)

    session = Session()
    try:
        # preparations dimensions uniques
        genres = {}
        publishers = {}
        platforms = {}

        # Genre
        for i, row in CSV_df.iterrows():
            genre = row["Genre"]
            if genre not in genres:
                genre_objet = models.Genre(type_genre=genre)
                session.add(genre_objet)
                session.flush() # force la recuperation d'id_genre
                genres[genre] = genre_objet

            # Publisher
            publisher = row['Publisher']
            if publisher not in publishers:
                publisher_objet = models.Publisher(name_publisher=publisher)
                session.add(publisher_objet)
                session.flush() # force la recuperation d'id_publisher
                publishers[publisher] = publisher_objet

            # Platform
            platform = row('Platform')
            if platform not in platforms:
                platform_objet = models.platform(name_platform=platform)
                session.add(platform_objet)
                session.flush() # force la recuperation d'id_platform
                platforms[platform] 

        session.commit()

        # ajouts des Games et des Sales
        for i, row in CSV_df.iterrows():
            genre_objet = genres[row['Genre']]
            publisher_objet = publishers[row['Publisher']]
            platform_objet = platforms[row['Platforms']]

            # Games
            game = models.Game(
                rank_game = int(row['Rank']),
                name_game = row['Name'],
                id_genre_fk = genre_objet.id_genre,
                id_publisher_fk = publisher_objet.id_publisher
            )
            session.add(game)
            session.flush()

            # Game_Platform
            year = int(row['Year']) if not pd.isnull(row['Year']) else None # dans le csv la date peut etre nulle
            game_platform = models.Game_Platform(
                id_game = game.id_game,
                id_platform = platform_objet.id_platform,
                release_year = year
            )
            session.add(game_platform)

            # Sales
            
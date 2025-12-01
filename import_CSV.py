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

            # publisher = row['Publisher']
            # publisher_name peut etre null dans le csv 
            # if pd.isna(publisher):
            #    publisher = None
            publisher = None if pd.isna(row['Publisher']) else row['Publisher']

            if publisher not in publishers:
                publisher_objet = models.Publisher(name_publisher=publisher)
                session.add(publisher_objet)
                session.flush() # force la recuperation d'id_publisher
                publishers[publisher] = publisher_objet

            # Platform
            platform = row['Platform']
            if platform not in platforms:
                platform_objet = models.Platform(name_platform=platform)
                session.add(platform_objet)
                session.flush() # force la recuperation d'id_platform
                platforms[platform] = platform_objet

        session.commit()

        # ajouts des Games et des Sales
        for i, row in CSV_df.iterrows():
            # on remplace par None les champs vides dans le csv pour le name_genre name_publisher name_platform            
            genre_objet = genres[row['Genre']] if not pd.isna(row['Genre']) else None
            publisher_objet = publishers[row['Publisher']] if not pd.isna(row['Publisher']) else None
            platform_objet = platforms[row['Platform']] if not pd.isna(row['Platform']) else None

            # Games
            game = models.Game(
                rank_game = int(row['Rank']),
                name_game = row['Name'],
                # remplace la clé etrangere par None si vide dans le csv
                id_genre_fk = genre_objet.id_genre if genre_objet else None,
                id_publisher_fk = publisher_objet.id_publisher if publisher_objet else None
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
            sale = models.Sale(
                NA_sale = row.get('NA_Sales', 0),
                EU_sale = row.get('EU_Sales',0),
                JP_sale = row.get('JP_Sales', 0),
                Other_sale = row.get('Other_Sales', 0),
                Global_sale = row.get('Global_Sales', 0),
                id_game_fk = game.id_game
            )
            session.add(sale)

        session.commit()
        print('Import de vgsales.csv reussi')
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f'Erreur SQLAlchemy: {e}')
    finally:
        session.close()

if __name__ == '__main__':
    populate_from_CSV(CSV_path)
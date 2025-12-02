from sqlalchemy.exc import SQLAlchemyError
from database import Session
import models

def input_sale_data(session):
    games = session.query(models.Game).all()
    if not games:
        print('Aucun jeu disponible impossible de créer une sale')
        return None
    
    print('Listes des jeux')
    for g in games:
        print(f"ID {g.id_game} - {g.name_game}")

    while True:
        game_id_str = input("Entrez l'ID du jeu associé: ").strip()
        if not game_id_str:
            print('ID invalide, entier requis')
            continue
        game_id = int(game_id_str) # id_fk a retourner
        if any(g.id_game == game_id for g in games):
            break
        else:
            print('ID invalide, non trouvé')
    # input des float pour les differentes localités des ventes NA JP EU etc avec verification
    def sale_amount(col):
        while True:
            val_str = input(f"Saisissez {col} (float, 0 possible): ").strip()
            if val_str =='':
                return 0.0
            try:
                return float(val_str)
            except ValueError:
                print('Valeur invalide, saisissez un float')

    na = sale_amount('NA_Sale')
    eu = sale_amount('EU_sale')
    jp = sale_amount('JP_sale')
    other =sale_amount('Other_sale')
    glob = sale_amount('Global_sale')

    return {
        'NA_Sale': na,
        'EU_sale': eu,
        'JP_Sale': jp,
        'Other_Sale': other,
        'Global_Sale': glob,
        'id_game_fk': game_id
    }
    
# Create
def create_sale():
    session = Session()
    try:
        data = input_sale_data(session)
        if data is None:
            return
        sale = models.Sale(**data)
        session.add(sale)
        session.commit()
        print(f"Sale ID {sale.id_sale} créée pour le jeu ID {sale.id_game_fk}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'ajout de la sale: {e}")
    finally:
        session.close()
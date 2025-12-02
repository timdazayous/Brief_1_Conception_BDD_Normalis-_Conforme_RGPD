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
        'NA_sale': na,
        'EU_sale': eu,
        'JP_sale': jp,
        'Other_sale': other,
        'Global_sale': glob,
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

# Read
def read_sale():
    session = Session()
    try:
        print("=== Options d'affichage des Sales ===")
        print("1. Toutes les sales")
        print("2. Sale par ID")
        print("3. Sales d'un jeu (par ID de jeu)")
        choix = input("Choix (1-3) : ").strip()

        if choix == '1':
            sales = session.query(models.Sale).all()
            print(f'listes des {len(sales)} sales')
            for s in sales:
                game = s.game # on recupere lobjet complet grace la relation entre game et sale
                name = game.name_game if game else 'N/A'
                print(f'ID {s.id_sale} - Jeu {s.id_game_fk} {name} - NA_sales {s.NA_sale} - EU_sales {s.EU_sale} - JP_sales {s.JP_sale} - Other_sales {s.Other_sale} - Global_sales {s.Global_sale}')
        elif choix == '2':
            sale_id_str = input('ID de la sale: ').strip()
            if not sale_id_str.isdigit():
                print('ID invalide')
                return
            sale = session.get(models.Sale, int(sale_id_str))
            if not sale:
                print('ID invalide sale inexistante')
                return
            game = sale.game
            name = game.name_game if game else 'N/A'
            print(f'ID {sale.id_sale} - Jeu {sale.id_game_fk} {name} - NA_sales {sale.NA_sale} - EU_sales {sale.EU_sale} - JP_sales {sale.JP_sale} - Other_sales {sale.Other_sale} - Global_sales {sale.Global_sale}')
        elif choix == '3':
            game_id_str = input('ID du jeu: ').strip()
            if not game_id_str.isdigit():
                print('ID invalide')
                return
            game_id = int(game_id_str)
            sales = session.query(models.Sale).filter(models.Sale.id_game_fk == game_id).all()
            print(f'Liste des {len(sales)} sale(s) pour le jeu ID {game_id}')
            for s in sales:
                # normalement game existera tjr au vu des cardinalités et donc de la structure meme de ma bdd si je lai bien faite
                game_name = s.game.name_game if s.game else 'N/A'
                print(f'ID {s.id_sale} - Jeu {s.id_game_fk} {game_name} - NA_sales {s.NA_sale} - EU_sales {s.EU_sale} - JP_sales {s.JP_sale} - Other_sales {s.Other_sale} - Global_sales {s.Global_sale}')

        else:
            print('Choix invalide')
    except Exception as e:
        print(f'Erreur lors du read_sale: {e}')
    finally:
        session.close()

# Update
def update_sale():
    session = Session()
    try:
        sale_id_str = input('ID de la sale à modifier').strip()
        if not sale_id_str.isdigit():
            print('ID invalide')
            return
        sale = session.get(models.Sale, int(sale_id_str))
        if not sale:
            print('Id invalide Sale introuvable')
            return
        print(f'Sale à modifiée ID {sale.id_sale} - ID jeu {sale.id_game_fk} {sale.game.name_game} - NA_sales {sale.NA_sale} - EU_sales {sale.EU_sale} - JP_sales {sale.JP_sale} - Other_sales {sale.Other_sale} - Global_sales {sale.Global_sale}')

        def sale_amount_update(col_name, col_obj):
            val_str = input(f"{col_name} actuel = {col_obj} - saisissez la nouvelle valeur (entrée pour passer ou valider)").strip()
            if val_str == '':
                return col_obj, False
            try:
                return float(val_str), True
            except ValueError:
                print('Valeur invalide, pas de modifications')
                return col_obj, False
        
        updated = False
        sale.NA_sale, modified = sale_amount_update('NA_sale', sale.NA_sale)
        # updated prend True si lui ou si modified est True
        updated = updated or modified
        sale.JP_sale, modified = sale_amount_update('JP_sale', sale.JP_sale)
        # updated prend True si lui ou si modified est True
        updated = updated or modified
        sale.EU_sale, modified = sale_amount_update('EU_sale', sale.EU_sale)
        # updated prend True si lui ou si modified est True
        updated = updated or modified
        sale.Other_sale, modified = sale_amount_update('Other_sale', sale.Other_sale)
        # updated prend True si lui ou si modified est True
        updated = updated or modified
        sale.Global_sale, modified = sale_amount_update('Gloabl_sale', sale.Global_sale)
        # updated prend True si lui ou si modified est True
        updated = updated or modified    

        # modification du jeu lié a la sale
        change_game = input('Changer le jeu lié ? (oui/non, yes/no): ').strip().lower()
        if change_game in ('oui', 'yes'):
            games = session.query(models.Game).all()
            for g in games:
                print(f"ID {g.id_game} - {g.name_game}")
            game_id_str = input("Saisissez l'ID du nouveau jeu").strip()
            if game_id_str.isdigit():
                game_id = int(game_id_str)
                if any(g.id_game == game_id for g in games):
                    sale.id_game_fk = game_id
                    updated = True
                else:
                    print('ID jeu invalide, pas de modification du jeu')
            else:
                print('ID invalide, pas de modifications')
        if updated:
            session.commit()
            print('Sale mise à jour reussie')
        else:
            print('Aucunes modifications apportées à sale')
    except SQLAlchemyError as e:
        print(f"Erreur lors de l'updatede sale: {e}")
        session.rollback()
    finally:
        session.close()

# Delete
def delete_user():
    print('hello world')
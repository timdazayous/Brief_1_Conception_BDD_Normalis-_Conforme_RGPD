from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from database import Session
import bcrypt
import re
import hashlib

def hash_password(password):
    """hash un password avec bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def hash_email(email):
    """hash l'email via SHA256 en minuscule et sans espaces"""
    email_clean = email.lower().strip()
    return hashlib.sha256(email_clean.encode('utf-8')).hexdigest()

def is_valid_email(email):
    """Controle email valide via regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_safe_input(prompt, input_type='str', min_len=None, max_len=None, choices=None, allow_empty=False):
    """controle de saisie generique prise en compte des attributs pouvant etre vides"""
    while True:
        value = input(prompt).strip()
        if not value and allow_empty:
            return None
        if not value:
            print('valeur obligatoire')
            continue
        if input_type == 'int':
            try:
                result = int(value)
                if min_len is not None and result < min_len:
                    print(f'valeur minimale: {min_len}')
                    continue
                return result
            except ValueError:
                print('saisissez un entier')
                continue
        elif input_type == 'email':
            if not is_valid_email(value):
                print('email invalide')
                continue
            return value
        elif input_type == 'str':
            if min_len is not None and len(value) < min_len:
                print(f'au moins {min_len} caractères à saisir')
                continue
            if max_len is not None and len(value) > max_len:
                print(f'au maximum {max_len} caractères à saisir')
                continue
            return value
        elif choices and value not in choices:
            print(f"choix possibles: {', '.join(choices)}")
            continue
        return value

def get_field_constraints(field_name):
    """contraintes specifiques par champ"""
    constraints = {
        'pseudo_user': {'max_len': 50},
        'name_game': {'max_len': 100},
        'name_publisher': {'max_len': 100},
        'name_platform': {'max_len': 30},
        'type_genre': {'max_len': 40},
        'rank_game': {'min_len': 1},
        'NA_sale': {'min_len': 0},
        'EU_sale': {'min_len': 0},
        'JP_sale': {'min_len': 0},
        'Other_sale': {'min_len': 0},
        'Global_sale': {'min_len': 0},
        'limitdate_user': {'min_len': 20260000},
    }
    return constraints.get(field_name, {})

def get_foreign_key_options(session, model, fk_field):
    mapper = inspect(model)
    rel = [r for r in mapper.relationships if fk_field in r.local_columns]
    if not rel:
        return None
    related_model = rel[0].mapper.class_
    options = session.query(related_model).all()
    return options

def display_options(options, display_field):
    if not options:
        print("aucune option disponible")
        return False
    print("options disponibles:")
    for opt in options:
        id_attr = next((a for a in opt.__dict__.keys() if a.startswith("id_")), None)
        if id_attr:
            print(f"ID {getattr(opt, id_attr)} - {getattr(opt, display_field)}")
    return True

def input_generic_data(session, model_class, exclude_fields=None):
    """Saisie générique des données d'une classe"""
    if exclude_fields is None:
        exclude_fields = []
    mapper = inspect(model_class)
    data = {}
    for column in mapper.attrs:
        if column.key in exclude_fields:
            continue
        # Ne traiter que les colonnes, pas les relations
        if not hasattr(column, 'columns'):
            continue
        if any(c.primary_key for c in column.columns):
            continue  # Exclure la clé primaire
        col_info = mapper.c[column.key]
        field_name = column.key.replace(f"{model_class.__tablename__.lower()}_", "")
        prompt = f"{field_name.replace('_', ' ').title()}: "
        constraints = get_field_constraints(column.key)
        min_len = constraints.get('min_len')
        max_len = constraints.get('max_len')

        if model_class.__name__ == 'User':
            if "password" in column.key:
                value = get_safe_input(prompt + "(sera hashé)", 'str', min_len=6)
                data[column.key] = hash_password(value)
                continue
            elif "mail" in column.key:
                value = get_safe_input(prompt, 'email')
                data[column.key] = hash_email(value)
                continue

        if "bool" in str(col_info.type):
            while True:
                val = input(prompt + "(oui/non yes/no): ").strip().lower()
                if val in ['oui', 'yes']:
                    data[column.key] = True
                    break
                elif val in ['non', 'no']:
                    data[column.key] = False
                    break
                print("oui/non requis")

        elif "Integer" in str(col_info.type):
            data[column.key] = get_safe_input(prompt, 'int', min_len=min_len)

        elif "String" in str(col_info.type):
            data[column.key] = get_safe_input(prompt, 'str', min_len=min_len, max_len=max_len)

        else:
            fk_options = get_foreign_key_options(session, model_class, column.key)
            if fk_options and len(fk_options) > 0:
                if display_options(fk_options, field_name):
                    while True:
                        opt_id = input("ID (ou entrée pour passer): ").strip()
                        if not opt_id:
                            break
                        if opt_id.isdigit():
                            data[column.key] = int(opt_id)
                            break
                        print("ID numérique (ou entrée pour passer)")
            else:
                data[column.key] = get_safe_input(prompt, 'str', min_len=min_len, max_len=max_len)

    return data

def create_generic(model_class, model_name):
    session = Session()
    try:
        print(f'=== Création {model_name} ===')
        data = input_generic_data(session, model_class)
        instance = model_class(**data)
        session.add(instance)
        session.flush()
        session.commit()
        print(f'{model_name} créé avec succès !')
    except SQLAlchemyError as e:
        session.rollback()
        print(f'erreur création {e}')
    except Exception as e:
        session.rollback()
        print(f'erreur: {e}')
    finally:
        session.close()

def read_generic(model_class, model_name):
    """read générique sans affichage mail/password par respect du RGPD"""
    session = Session()
    try:
        print(f"=== Lecture {model_name} ===")
        print("1. tous | 2. par ID")
        choice = get_safe_input("choix (1-2): ", 'str', choices=['1','2'])
        if choice == '1':
            instances = session.query(model_class).all()
            print(f"{len(instances)} enregistrements trouvés:")
            for inst in instances:
                if model_name.lower() == 'user':
                    print(f"ID {inst.id_user} - pseudo {inst.pseudo_user}")
                else:
                    # Afficher les attributs principaux lisiblement s’ils existent
                    name_attr = next((k for k in inst.__dict__ if 'name' in k.lower() or 'pseudo' in k.lower()), None)
                    if name_attr:
                        id_attr = next((a for a in inst.__dict__.keys() if a.startswith("id_")), None)
                        print(f"ID {getattr(inst, id_attr)} - {getattr(inst, name_attr)}")
                    else:
                        print(inst)
        elif choice == '2':
            id_val = get_safe_input("ID: ", 'int')
            instance = session.get(model_class, id_val)
            if instance:
                print(instance)
            else:
                print("non trouvé")
    except Exception as e:
        print(f"erreur lecture: {e}")
    finally:
        session.close()


def update_generic(model_class, model_name):
    session = Session()
    try:
        print(f"=== Modification {model_name} ===")
        id_val = get_safe_input(f"ID {model_name}: ", 'int')
        instance = session.get(model_class, id_val)
        if not instance:
            print("non trouvé")
            return
        print(f"Trouvé: {str(instance)}")
        data = input_generic_data(session, model_class)
        updated = False
        for field, value in data.items():
            if getattr(instance, field, None) != value:
                setattr(instance, field, value)
                updated = True
        if updated:
            session.commit()
            print(f"{model_name} mis à jour")
        else:
            print("aucun changement")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"erreur update: {e}")
    finally:
        session.close()

def delete_generic(model_class, model_name):
    session = Session()
    try:
        print(f"=== Suppression {model_name} ===")
        id_val = get_safe_input(f"ID {model_name}: ", 'int')
        instance = session.get(model_class, id_val)
        if not instance:
            print("non trouvé")
            return
        print(f"À supprimer: {str(instance)}")
        confirm = get_safe_input("Confirmer ? (oui/non): ", 'str', choices=['oui', 'non'])
        if confirm.lower() == 'oui':
            session.delete(instance)
            session.commit()
            print(f"{model_name} supprimé")
        else:
            print("suppression annulée")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"erreur suppression: {e}")
    finally:
        session.close()

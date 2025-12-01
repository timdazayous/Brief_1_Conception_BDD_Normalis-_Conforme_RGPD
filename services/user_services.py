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
        session.commit()
        print(f'User {user.pseudo_user} créé')
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'ajout du nouvel user: {e}")

def read_user():
    session = Session()
    try:
        pseudo_user = input('Pseudo à afficher: ')
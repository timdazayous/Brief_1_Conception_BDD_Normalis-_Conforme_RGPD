import models
from services.crud_generic import (
    create_generic, read_generic, update_generic, delete_generic
)

MODELS = [
    models.User, models.Game, models.Sale, models.Publisher,
    models.Platform, models.Genre, models.User_Game, models.Game_Platform
]

MODEL_NAMES = {
    models.User: "User",
    models.Game: "Game", 
    models.Sale: "Sale",
    models.Publisher: "Publisher",
    models.Platform: "Platform",
    models.Genre: "Genre",
    models.User_Game: "User_Game",
    models.Game_Platform: "Game_Platform"
}

def display_models():
    """affiche la liste des tables"""
    print("\n=== TABLES DISPONIBLES ===")
    for i, model_class in enumerate(MODELS, 1):
        print(f"{i}. {MODEL_NAMES[model_class]}")

def get_model_choice():
    """retourne la table choisie ou None"""
    display_models()
    while True:
        try:
            choice = int(input("\nChoisissez (1-8) ou 0=Quitter: "))
            if choice == 0:
                return None
            if 1 <= choice <= len(MODELS):
                return MODELS[choice - 1]
            print("choix invalide (0-8)")
        except ValueError:
            print("entier requis (0-8)")

def display_crud_menu(model_name):
    """affiche menu CRUD"""
    print(f"\n=== CRUD {model_name} ===")
    print("1. Créer")
    print("2. Lire") 
    print("3. Modifier")
    print("4. Supprimer")
    print("0. Retour")

def run_crud_interface(model_class):
    """interface CRUD complète pour une table"""
    model_name = MODEL_NAMES[model_class]
    
    while True:
        display_crud_menu(model_name)
        choice = input("Choix (0-4): ").strip()
        
        if choice == '1':
            create_generic(model_class, model_name)
        elif choice == '2':
            read_generic(model_class, model_name)
        elif choice == '3':
            update_generic(model_class, model_name)
        elif choice == '4':
            delete_generic(model_class, model_name)
        elif choice == '0':
            break
        else:
            print("choix invalide")

def run_app():
    """lance l'application complète"""
    print("SYSTÈME CRUD GÉNÉRIQUE")
    while True:
        model_class = get_model_choice()
        if model_class is None:
            print("à bientôt !")
            break
        run_crud_interface(model_class)

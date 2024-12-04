import requests
import traceback
import time

def check_server_availability(url, timeout=30):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                return True
            else:
                print(f"Erreur HTTP : {response.status_code}")
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return False

def main():
    url = 'https://www.seculeague.link'
    
    # Vérification de la disponibilité du serveur avec curl
    print("Vérification de la disponibilité du serveur avec curl...")
    
    if not check_server_availability(url):
        print("Le serveur n'est pas disponible. Arrêt du script.")
        return

    # Si le serveur est disponible, vous pouvez effectuer d'autres actions ici
    print("Le serveur est disponible. Vous pouvez maintenant effectuer des actions supplémentaires.")

    # Exemple d'envoi d'une requête GET pour accéder à une page spécifique
    try:
        response = requests.get(url, verify=False)
        print("Contenu de la page :")
        print(response.text[:500])  # Affiche les 500 premiers caractères du contenu
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'accès à la page : {str(e)}")
        print("Traceback complet:")
        traceback.print_exc()

if __name__ == "__main__":
    main()

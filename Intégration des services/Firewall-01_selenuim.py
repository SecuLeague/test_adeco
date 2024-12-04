import requests

# Remplacez par l'adresse IP de votre pfSense
url = 'https://http://172.16.150.2//api/v1/'
username = 'admin'
password = 'pfsense'

# Vérifier la disponibilité du serveur
try:
    response = requests.get(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        print("Connexion réussie à pfSense!")
        # Vous pouvez maintenant faire d'autres appels API ici
    else:
        print(f"Erreur lors de la connexion : {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Une erreur s'est produite : {e}")

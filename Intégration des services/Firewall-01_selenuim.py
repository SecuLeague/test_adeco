import subprocess
import sys
import requests
import time

def check_server_availability(url, timeout=30):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                return True
            time.sleep(5)
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return False

def main():
    try:
        print("Vérification de la disponibilité du serveur...")
        if not check_server_availability('https://172.16.150.2', timeout=30):
            print("Le serveur n'est pas accessible après plusieurs tentatives. Vérifiez votre connexion réseau.")
            return

        print("Tentative de connexion à pfSense...")
        curl_command = [
            "curl",
            "-k",  # Ignorer la vérification SSL
            "-X", "POST",
            "-c", "cookies.txt",  # Sauvegarder les cookies
            "-d", "login=Login&usernamefld=admin&passwordfld=pfsense&__csrf_magic=sid%3A0123456789abcdef0123456789abcdef",
            "https://172.16.150.2/index.php"
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True)

        if result.returncode == 0:
            print("Connexion réussie")
            print(result.stdout)
        else:
            print("Erreur lors de la connexion")
            print(result.stderr)

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    main()

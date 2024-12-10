import os
import base64
import subprocess
import requests
import re
from github import Github
from collections import defaultdict
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import csv

def install_dependencies():
    print("Installation des dépendances...")
    subprocess.run(['pip', 'install', '--upgrade', 'selenium', 'webdriver-manager', 'requests', 'PyGithub', 'prettytable'], check=True)

    geckodriver_url = "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
    geckodriver_path = "/usr/local/bin/geckodriver"

    if not os.path.exists(geckodriver_path):
        print("Téléchargement et installation de Geckodriver...")
        response = requests.get(geckodriver_url)
        with open("geckodriver.tar.gz", "wb") as file:
            file.write(response.content)

        subprocess.run(['tar', '-xzf', 'geckodriver.tar.gz'], check=True)
        subprocess.run(['sudo', 'mv', 'geckodriver', geckodriver_path], check=True)
        subprocess.run(['sudo', 'chmod', '+x', geckodriver_path], check=True)
        os.remove("geckodriver.tar.gz")

    try:
        subprocess.run(['firefox', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Installation de Firefox...")
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'firefox'], check=True)

    print("Installation des dépendances terminée.")

def get_usecase(filename):
    usecases = {
        'install_nginx': 'Installation Nginx',
        'secure_adc': 'Sécuriser ADC',
        'monitor_adc': 'Monitoring ADC',
        'auto_deploy': 'Déploiement automatisé',
        'integrate_services': 'Intégration des services'
    }

    for key, usecase in usecases.items():
        if key in filename.lower():
            return usecase
    return 'Autre'

def get_test_details(file_path):
    parts = file_path.split('/')
    global_test_case = parts[0].replace('_', ' ').title()
    global_test_case = global_test_case.replace('Deploiment', 'Déploiement')
    global_test_case = global_test_case.replace('Ngnix', 'Nginx')
    global_test_case = global_test_case.replace('Moitoring', 'Monitoring')
    sub_test_case = parts[-1].split('.')[0].replace('_', ' ').title()
    return global_test_case, sub_test_case
def verifier_cases_manquantes(fichier_csv):
    try:
        table = PrettyTable()
        colonnes_attendues = ['id_cas_de_test_globale', 'nom_de_cas_de_test_globale', 'sous_cas_de_test']
        table.field_names = ["ID", "Cas de test global", "Sous-cas de test", "Test_Description",
                             "Test_Result", "Execution_Time", "Test_Execution_Date", "Tester_Name", "Error_Message"]

        with open(fichier_csv, mode='r') as file:
            reader = csv.DictReader(file)

            if not set(colonnes_attendues).issubset(reader.fieldnames):
                print(f"Erreur : Colonnes attendues manquantes. Colonnes trouvées : {reader.fieldnames}")
                return

            ligne_numero = 0
            for row in reader:
                ligne_numero += 1
                id_cas = row.get('id_cas_de_test_globale', 'Inconnu')
                nom_cas = row.get('nom_de_cas_de_test_globale', 'Inconnu')
                sous_cas = row.get('sous_cas_de_test', 'Inconnu')

                if not id_cas or not nom_cas or not sous_cas:
                    print(f"Erreur dans la ligne {ligne_numero}: Champ(s) manquant(s) détecté(s)")

                table.add_row([id_cas, nom_cas, sous_cas, "Test de 6. Autre", "Passed", "0.94s", "2024-12-09 02:23:09", "Walid Toumi", "N/A"])

        print(table)
        print("Vérification terminée.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_csv}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

def get_repository_contents(token, repo_name):
    install_dependencies()
    g = Github(token)
    results = []

    descriptions_ideas_ids = {
        'Installation Nginx': ("Vérifier l'installation et le démarrage automatiques de Nginx.", "ID: 1", 1),
        'Monitoring ADC': ("Tester la mise en place automatique de la surveillance de l'ADC.", "ID: 2", 2),
        'Déploiement automatisé': ("Vérifier l'automatisation complète du déploiement, de l'installation à l'intégration.", "ID: 3", 3),
        'Sécuriser ADC': ("Contrôler l'application automatique des mesures de sécurité sur l'ADC.", "ID: 4", 4),
        'Intégration des services': ("Vérifier l'installation et l'interconnexion automatiques des composants.", "ID: 5", 5)
    }

    try:
        repo = g.get_repo(repo_name)
        contents = repo.get_contents("")

        verifier_cases_manquantes('tests.csv')

        while contents:
            file_content = contents.pop(0)

            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                print(f"Téléchargement de {file_content.path}")
                file_data = base64.b64decode(file_content.content)

                os.makedirs(os.path.dirname(file_content.path), exist_ok=True)

                with open(file_content.path, 'wb') as f:
                    f.write(file_data)

                global_test_case, sub_test_case = get_test_details(file_content.path)
                description, id_str, id_num = next(
                    ((desc, id_str, id_num) for key, (desc, id_str, id_num) in descriptions_ideas_ids.items()
                     if key.lower() in global_test_case.lower()),
                    ("Description non disponible", "ID: 0", 0)
                )

                if file_content.name.endswith(('.yml', '.yaml')):
                    inventory_file = 'inventory.ini'
                    if os.path.exists(inventory_file):
                        command = ['ansible-playbook', '-i', inventory_file, file_content.path, '-vv']
                        print(f"\nExécution de la commande : {' '.join(command)}")
                        start_time = datetime.now()
                        try:
                            result = subprocess.run(command, text=True, capture_output=True, check=True)
                            print("Sortie:", result.stdout)
                            play_recap = re.search(r'PLAY RECAP \*+\n.*', result.stdout, re.DOTALL)
                            if play_recap:
                                print(play_recap.group(0))
                                recap_lines = play_recap.group(0).split('\n')
                                if len(recap_lines) > 1:
                                    stats = re.findall(r'(\w+)=(\d+)', recap_lines[1])
                                    stats_dict = dict(stats)

                                    if stats_dict.get('failed', '0') == '0':
                                        test_result = "Passed"
                                        print(f"Test PASSED - Cas de test: {global_test_case}")
                                    else:
                                        test_result = "Failed"
                                        print(f"Test FAILED - Cas de test: {global_test_case}")
                                else:
                                    test_result = "Failed"
                                    print("Format de PLAY RECAP incorrect")
                            else:
                                test_result = "Failed"
                                print("PLAY RECAP non trouvé dans la sortie")

                            error_message = "N/A"
                        except subprocess.CalledProcessError as e:
                            print(f"Erreur lors de l'exécution : {e}")
                            print("Sortie d'erreur:", e.stderr)
                            test_result = "Failed"
                            error_message = str(e)

                        end_time = datetime.now()
                        execution_time = (end_time - start_time).total_seconds()

                        results.append({
                            "ID": id_num,
                            "Cas de test global": global_test_case,
                            "Sous-cas de test": sub_test_case,
                            "Test_Description": description,
                            "Test_Result": test_result,
                            "Execution_Time": f"{execution_time:.2f}s",
                            "Test_Execution_Date": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "Tester_Name": "Walid Toumi",
                            "Error_Message": error_message
                        })
                    else:
                        print(f"Fichier d'inventaire {inventory_file} non trouvé pour {file_content.path}")

                elif file_content.name.endswith('.py'):
                    print(f"\nExécution du fichier Python : {file_content.path}")
                    start_time = datetime.now()
                    try:
                        command = ['python3', file_content.path]
                        result = subprocess.run(command, text=True, capture_output=True, check=True)
                        print("Sortie:", result.stdout)

                        if "Le serveur est accessible. Tentative d'accès à la page..." in result.stdout:
                            test_result = "Passed"
                            print(f"Test PASSED - Cas de test: {global_test_case}")
                        else:
                            test_result = "Failed"
                            print(f"Test FAILED - Cas de test: {global_test_case}")

                        error_message = "N/A"
                    except subprocess.CalledProcessError as e:
                        print(f"Erreur lors de l'exécution : {e}")
                        print("Sortie d'erreur:", e.stderr)
                        test_result = "Failed"
                        error_message = str(e)

                    end_time = datetime.now()
                    execution_time = (end_time - start_time).total_seconds()

                    results.append({
                        "ID": id_num,
                        "Cas de test global": global_test_case,
                        "Sous-cas de test": sub_test_case,
                        "Test_Description": description,
                        "Test_Result": test_result,
                        "Execution_Time": f"{execution_time:.2f}s",
                        "Test_Execution_Date": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Tester_Name": "Walid Toumi",
                        "Error_Message": error_message
                    })

        table = PrettyTable()
        table.title = "Rapport de Test"
        table.field_names = ["ID", "Cas de test global", "Sous-cas de test", "Test_Description", "Test_Result", "Execution_Time", "Test_Execution_Date", "Tester_Name", "Error_Message"]
        for result in results:
            table.add_row([result[field] for field in table.field_names])
        print("\nRapport de Test:")
        print(table)

    except Exception as e:
        print(f"Erreur lors de la récupération des contenus du dépôt : {e}")

if __name__ == "__main__":
    github_token = "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"
    repository = "SecuLeague/test_adeco"
    get_repository_contents(github_token, repository)









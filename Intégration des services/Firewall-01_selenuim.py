import asyncio
import aiohttp
import traceback

async def check_server_availability(url, timeout=10):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout, ssl=False) as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False

async def main():
    url = 'http://172.16.150.2/'  # URL à vérifier
    
    try:
        print("Vérification de la disponibilité du serveur...")
        
        if not await check_server_availability(url):
            print("Le serveur n'est pas accessible. Vérifiez votre connexion réseau.")
            return
        
        print("Le serveur est accessible. Tentative d'accès à la page...")

        # Accéder à la page et afficher le contenu
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    content = await response.text()
                    print("Contenu de la page :")
                    print(content[:500])  # Affiche les 500 premiers caractères du contenu
                else:
                    print(f"Erreur lors de l'accès à la page : {response.status}")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        print("Traceback complet:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

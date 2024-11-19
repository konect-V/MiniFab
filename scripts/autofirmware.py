import subprocess
import re
import time

def get_canbus_uuid():
    # Commande à exécuter
    command = "~/klippy-env/bin/python ~/klipper/scripts/canbus_query.py can0"
    
    try:
        # Exécution de la commande
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        # Vérification des erreurs
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de la commande : {result.stderr}")
            return None
        
        # Extraction des UUIDs avec une regex
        uuids = re.findall(r"canbus_uuid=([a-fA-F0-9]+)", result.stdout)
        return uuids
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def main():    
    while True:
        uuids = get_canbus_uuid()
        
        if uuids:
            for uuid in uuids:
                print(f"UUID trouvé : {uuid}")
        
        # Attends
        time.sleep(30)

if __name__ == "__main__":
    main()

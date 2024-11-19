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
        print(uuids)
        return uuids
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def main():
    # Liste pour stocker les UUIDs uniques trouvés
    seen_uuids = set()
    
    while True:
        print("Exécution de la commande...")
        uuids = get_canbus_uuid()
        
        if uuids:
            for uuid in uuids:
                if uuid not in seen_uuids:
                    print(f"UUID trouvé : {uuid}")
                    seen_uuids.add(uuid)
        else:
            print("Aucun UUID trouvé ou erreur lors de l'exécution.")
        
        # Attends
        time.sleep(5)

if __name__ == "__main__":
    main()

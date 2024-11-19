import subprocess
import re
import os
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


def extract_canbus_uuids():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, "../config")
    uuid_mapping = {}

    for folder in os.listdir(config_dir):
        folder_path = os.path.join(config_dir, folder)
        printer_cfg_path = os.path.join(folder_path, "printer.cfg")

        # Vérifie que c'est un dossier et qu'il contient un fichier printer.cfg
        if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
            try:
                with open(printer_cfg_path, 'r') as file:
                    content = file.read()
                
                # Extraction de tous les canbus_uuid dans le fichier
                uuids = re.findall(r"canbus_uuid:\s*([a-fA-F0-9]+)", content)
                
                if uuids:
                    uuid_mapping[folder] = uuids
            except Exception as e:
                print(f"Erreur en lisant {printer_cfg_path}: {e}")
    
    return uuid_mapping

def find_folder_by_uuid(uuid, uuid_mapping):
    for folder, uuids in uuid_mapping.items():
        if uuid in uuids:
            return folder
    return None

def main():
    uuid_mapping = extract_canbus_uuids()

    # set at iddle state first
    script_dir = os.path.dirname(os.path.abspath(__file__))
    confswap_executable_path = os.path.join(script_dir, "./confswap.py")
    os.system("python confswap.py iddle")
    os.system('sudo systemctl restart klipper')

    while True:
        uuids = get_canbus_uuid()
        
        if uuids:
            for uuid in uuids:
                machine = find_folder_by_uuid(uuid, uuid_mapping)
                t = 0

                if machine == "mill":
                    t = 1
                elif machine == "print":
                    t = 2
                elif machine == "penplt":
                    t = 3
                else:
                    print(f"Unknown: {machine}")

                if t != 0:
                    print(f"Changement de firmware pour : {machine}")

                    command = f"curl -d \"script=M453 T{t}\" http://127.0.0.1/printer/gcode/script"
                    result = subprocess.run(command, shell=True, text=True, capture_output=True)

                    if result.returncode != 0:
                        print(f"Erreur lors de l'exécution de la commande de changement de firmware : {result.stderr}")
                        return None
        time.sleep(30)

if __name__ == "__main__":
    main()

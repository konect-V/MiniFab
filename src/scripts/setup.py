import subprocess
import os

is_kiauh = 0
user_dir = "/home/minifab"
repo_dir = os.path.join(user_dir, "MiniFab")

def ask_confirmation():
    while True:
        response = input("As-tu bien lu les instructions pour installer gcode_shell_command ? (oui/non) : ").strip().lower()
        if response == "oui":
            return True
        elif response == "non":
            print("Merci de lire les instructions avant de continuer.")
        else:
            print("Réponse invalide. Merci de répondre par 'oui' ou 'non'.")

def install_kiauh():
    global is_kiauh

    if is_kiauh == 1:
        return
    
    try:
        # Step 1: Update system and install git if not already installed
        print("Updating system and installing git...")
        subprocess.run(["sudo", "pip", "install", "flask"], check=True)
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "git", "-y"], check=True)
        
        # Step 2: Clone KIAUH repository into the home directory
        kiauh_path = os.path.expanduser("~/kiauh")
        if not os.path.isdir(kiauh_path):
            print("Cloning KIAUH repository into the home directory...")
            subprocess.run(["git", "clone", "https://github.com/dw-0/kiauh.git", kiauh_path], check=True)
            print("KIAUH installation completed.")
        else:
            print("KIAUH is already installed in the home directory.")
        
        print("KIAUH installation completed.")

        print_area_bed_mesh_path = os.path.expanduser("~/print_area_bed_mesh")
        subprocess.run(["git", "clone", "https://github.com/Turge08/print_area_bed_mesh.git", print_area_bed_mesh_path], check=True)

        os.chdir(kiauh_path)

        # Installer gcode_shell_command à partir de KIAUH
        print("Suivez les instructions dans KIAUH pour installer KlipperScreen (utiliser xserver), OctoEverywhere (configurer avec un compte) et gcode_shell_command(B->Advanced->G Code Shell Command->Y->n->B->Q) à partir de KIAUH...")
        ask_confirmation()
        subprocess.run(["./kiauh.sh"], check=True)  # Lancement du script KIAUH pour accéder aux options d'installation

        is_kiauh = 1
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue : {e}")

def copy_config_files():
    source_dir = os.path.join(repo_dir, "src/config/")
    dest_dir = os.path.join(user_dir, "printer_data/")

    try:
        subprocess.run(f"cp -r {source_dir} {dest_dir}", shell=True, check=True)
        print(f"Les fichiers ont été copiés de {source_dir} vers {dest_dir}.")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de la copie des fichiers : {e}")

def reboot():
    os.system('systemctl reboot -i')

def update_config():
    try:
        print("Mise à jour du dépôt...")
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
        print("Mise à jour du dépôt terminée.")
        print("Mise à jour de la config...")
        copy_config_files()
        print("Mise à jour du config terminée.")
        os.system('sudo systemctl restart klipper')
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de la mise à jour du dépôt : {e}")


setup_status_file = "setup_status.txt"

def setup_config():
    # Code pour la configuration initiale
    print("Exécution du setup de la config...")
    install_kiauh()
    copy_config_files()
    # Simule la configuration
    with open(setup_status_file, "w") as f:
        f.write("setup_done")
    print("Setup terminé.")
    reboot()

def menu():
    # Vérifie si le setup a déjà été effectué en lisant le fichier de statut
    if os.path.exists(setup_status_file):
        with open(setup_status_file, "r") as f:
            status = f.read().strip()
        if status == "setup_done":
            print("Le setup a déjà été effectué. Passage à la mise à jour de la config.")
            update_config()
            return
        else:
            setup_config()
    else:
        setup_config()

if __name__ == '__main__':
    menu()

import subprocess
import os

is_kiauh = 0

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

        os.chdir(kiauh_path)

        # Installer gcode_shell_command à partir de KIAUH
        print("Suivez les instructions dans KIAUH pour installer gcode_shell_command(B->Advanced->G Code Shell Command->Y->n->B->Q) à partir de KIAUH...")
        ask_confirmation()
        subprocess.run(["./kiauh.sh"], check=True)  # Lancement du script KIAUH pour accéder aux options d'installation

        is_kiauh = 1
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def copy_config_files():
    source_dir = os.path.join(os.path.dirname(__file__), "config", "*")
    dest_dir = os.path.expanduser("~/printer_data/config")

    try:
        subprocess.run(f"cp -r {source_dir} {dest_dir}", shell=True, check=True)
        print(f"Les fichiers ont été copiés de {source_dir} vers {dest_dir}.")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de la copie des fichiers : {e}")

def reboot():
    os.system('systemctl reboot -i')

install_kiauh()
copy_config_files()
reboot()
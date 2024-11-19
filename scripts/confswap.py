import os
import sys

def create_symlink(src_file, dest_file):
    try:
        if os.path.islink(dest_file):
            os.unlink(dest_file)
        os.symlink(src_file, dest_file)
        print(f"Symlink crée: {src_file} -> {dest_file}")
    except Exception as e:
        print(f"Erreur {src_file}: {e}")

def main(config_name):
    base_path = os.path.expanduser("~/printer_data/config/")
    config_path = os.path.join(base_path, config_name)

    # Vérifie si le dossier existe
    if not os.path.isdir(config_path):
        print(f"Le dossier '{config_path}' n'existe pas dans {base_path}")
        return

    # Crée les liens symboliques
    create_symlink(os.path.join(config_path, "printer.cfg"), os.path.join(base_path, "printer.cfg"))
    create_symlink(os.path.join(config_path, "KlipperScreen.conf"), os.path.join(base_path, "KlipperScreen.conf"))
    print(f"Nouveau firmware pour : {config_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation: python script.py <config_folder_name>")
        sys.exit(1)
    
    config_folder = sys.argv[1]
    main(config_folder)

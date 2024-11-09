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
    base_path = "~/printer_data/config/"
    config_path = os.path.join(base_path, config_name)

    # Vérifie si le dossier existe
    if not os.path.isdir(config_path):
        print(f"Le dossier '{config_name}' n'existe pas dans {base_path}")
        return

    # Crée les liens symboliques
    create_symlink(os.path.join(config_path, "printer.cfg"), "printer.cfg")
    create_symlink(os.path.join(config_path, "KlipperScreen.conf"), "KlipperScreen.conf")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_folder_name>")
        sys.exit(1)
    
    config_folder = sys.argv[1]
    main(config_folder)

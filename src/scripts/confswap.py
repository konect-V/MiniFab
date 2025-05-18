import os
import sys

base_path = "/home/minifab/printer_data/config"

def create_symlink(src_file, dest_file):
    try:
        if os.path.exists(dest_file):
            if os.path.isfile(dest_file):
                os.remove(dest_file)
        if os.path.islink(dest_file):
            os.unlink(dest_file)
        os.symlink(src_file, dest_file)
        print(f"Symlink created: {src_file} -> {dest_file}")
    except Exception as e:
        print(f"Error {src_file}: {e}")

def confswap(config_name):
    config_path = os.path.join(base_path, "toolheads", config_name)

    # Check if the folder exists
    if not os.path.isdir(config_path):
        print(f"The folder '{config_path}' does not exist in {base_path}")
        return

    # Create the symlinks
    create_symlink(os.path.join(config_path, "printer.cfg"), os.path.join(base_path, "printer.cfg"))
    create_symlink(os.path.join(config_path, "KlipperScreen.conf"), os.path.join(base_path, "KlipperScreen.conf"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_folder_name>")
        sys.exit(1)
    
    config_folder = sys.argv[1]
    confswap(config_folder)
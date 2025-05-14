import subprocess
import os
import shutil

is_kiauh = 0
user_dir = "/home/minifab"
repo_dir = os.path.join(user_dir, "MiniFab")

def ask_confirmation():
    while True:
        response = input("Have you read the instructions for installing gcode_shell_command? (yes/no): ").strip().lower()
        if response == "yes":
            return True
        elif response == "no":
            print("Please read the instructions before continuing.")
        else:
            print("Invalid response. Please answer 'yes' or 'no'.")

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
        subprocess.run([os.path.join(print_area_bed_mesh_path, "/install.sh")], check=True)

        os.chdir(kiauh_path)

        # Install gcode_shell_command from KIAUH
        print("Follow the instructions in KIAUH to install KlipperScreen (use xserver), OctoEverywhere (configure with an account) and gcode_shell_command (B->Advanced->G Code Shell Command->Y->n->B->Q) from KIAUH...")
        ask_confirmation()
        subprocess.run(["./kiauh.sh"], check=True)  # Launch KIAUH script to access installation options

        is_kiauh = 1
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def copy_config_files():
    source_dir = os.path.join(repo_dir, "src/config/")
    dest_dir = os.path.join(user_dir, "printer_data/config/")
    
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    try:
        # Copy all files and directories recursively
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            if os.path.isdir(source_item):
                # For directories, copy recursively
                if os.path.exists(dest_item):
                    shutil.rmtree(dest_item)
                shutil.copytree(source_item, dest_item)
            else:
                # For files, just copy
                shutil.copy2(source_item, dest_item)
                
        print(f"Files have been copied from {source_dir} to {dest_dir}.")
    except Exception as e:
        print(f"An error occurred while copying files: {e}")

def reboot():
    os.system('systemctl reboot -i')

def update_config():
    try:
        print("Updating repository...")
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
        print("Repository update completed.")
        print("Updating configuration...")
        copy_config_files()
        print("Configuration update completed.")
        os.system('sudo systemctl restart klipper')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during repository update: {e}")


setup_status_file = "setup_status.txt"

def setup_config():
    # Code for initial configuration
    print("Executing config setup...")
    install_kiauh()
    copy_config_files()
    # Simulate configuration
    with open(setup_status_file, "w") as f:
        f.write("setup_done")
    print("Setup completed.")
    reboot()

def menu():
    # Check if setup has already been done by reading the status file
    if os.path.exists(setup_status_file):
        with open(setup_status_file, "r") as f:
            status = f.read().strip()
        if status == "setup_done":
            print("Setup has already been completed. Proceeding to update the configuration.")
            update_config()
            return
        else:
            setup_config()
    else:
        setup_config()

if __name__ == '__main__':
    menu()
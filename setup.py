import subprocess
import os

is_kiauh = 0

def install_kiauh():
    global is_kiauh

    if is_kiauh == 1:
        return
    
    is_kiauh = 1
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
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


install_kiauh()
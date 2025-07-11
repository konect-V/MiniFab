import subprocess
import os
import shutil
import argparse

is_kiauh = 0
user_dir = "/home/minifab"
repo_dir = os.path.join(user_dir, "MiniFab")

source_config_dir = os.path.join(repo_dir, "src/config/")
dest_config_dir = os.path.join(user_dir, "printer_data/config/")

klipperscreen_theme_path_source = os.path.join(repo_dir, "src/klipperscreen_theme")
klipperscreen_theme_path_dest = os.path.join(user_dir, "KlipperScreen/styles/minifab")

mainsail_theme_path_source = os.path.join(repo_dir, "src/mainsail_theme")
mainsail_theme_path_dest = os.path.join(dest_config_dir, ".theme")

print_area_bed_mesh_path = os.path.join(user_dir, "print_area_bed_mesh")
kiauh_path = os.path.join(user_dir, "kiauh")

setup_status_file = os.path.join(repo_dir, "setup_status.txt")

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
        if not os.path.isdir(kiauh_path):
            print("Cloning KIAUH repository into the home directory...")
            subprocess.run(["git", "clone", "https://github.com/dw-0/kiauh.git", kiauh_path], check=True)
            print("KIAUH installation completed.")
        else:
            print("KIAUH is already installed in the home directory.")
        
        print("KIAUH installation completed.")

        if not os.path.isdir(print_area_bed_mesh_path):
            print("Cloning print_area_bed_mesh repository...")
            subprocess.run(["git", "clone", "https://github.com/Turge08/print_area_bed_mesh.git", print_area_bed_mesh_path], check=True)
            subprocess.run([os.path.join(print_area_bed_mesh_path, "install.sh")], check=True)

        os.chdir(kiauh_path)

        # Install gcode_shell_command from KIAUH
        print("Follow the instructions in KIAUH to install KlipperScreen (use xserver), crowsnest, OctoEverywhere (configure with an account) and gcode_shell_command (B->Advanced->G Code Shell Command->Y->n->B->Q) from KIAUH...")
        ask_confirmation()
        subprocess.run(["./kiauh.sh"], check=True)  # Launch KIAUH script to access installation options

        is_kiauh = 1
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def copy_files(src, dest, clear):
    
    # Ensure destination directory exists
    os.makedirs(dest, exist_ok=True)

    try:
        if clear:
            # Remove existing files in the destination directory
            if os.path.exists(dest):
                shutil.rmtree(dest)

            # Create the destination directory again
            os.makedirs(dest, exist_ok=True)

        # Copy all files and directories recursively
        for item in os.listdir(src):
            source_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            
            if os.path.isdir(source_item):
                # For directories, copy recursively
                if os.path.exists(dest_item):
                    shutil.rmtree(dest_item)
                shutil.copytree(source_item, dest_item)
            else:
                # For files, just copy
                shutil.copy2(source_item, dest_item)
                
        print(f"Files have been copied from {src} to {dest}.")
    except Exception as e:
        print(f"An error occurred while copying files: {e}")


def update_config_files(clear_config):
    copy_files(source_config_dir, dest_config_dir, clear_config)
    copy_files(klipperscreen_theme_path_source, klipperscreen_theme_path_dest, clear_config)
    copy_files(mainsail_theme_path_source, mainsail_theme_path_dest, clear_config)

def reboot():
    os.system('systemctl reboot -i')

def update_config(clear_config):
    try:
        try:
            print("Updating repository...")
            subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
            print("Repository update completed.")
        except subprocess.CalledProcessError:
            print("Repository update failed.")
            
        print("Updating configuration...")
        update_config_files(clear_config)
        print("Configuration update completed.")
        os.system('sudo systemctl restart klipper')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during repository update: {e}")


def change_klipper_repo():
    repo_path = os.path.expanduser("~/klipper")
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Le répertoire {repo_path} n'existe pas.")
    
    try:
        subprocess.run(["git", "remote", "set-url", "origin", "https://github.com/konect-V/klipper"], cwd=repo_path, check=True)
        subprocess.run(["git", "fetch", "origin"], cwd=repo_path, check=True)
        subprocess.run(["git", "checkout", "minifab"], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while changing the Klipper repository: {e}")

def setup_config():
    # Code for initial configuration
    print("Executing config setup...")
    change_klipper_repo()
    install_kiauh()
    update_config_files(True)
    # Simulate configuration
    with open(setup_status_file, "w") as f:
        f.write("setup_done")
    print("Setup completed.")
    reboot()

def check_username():
    # Check if the username is "minifab"
    if os.environ.get('USER') != "minifab":
        print("This script must be run as the user 'minifab'.")
        return False
    return True

def check_dir():
    # Check if the directory exists
    if not os.path.exists(repo_dir):
        print(f"The directory {repo_dir} does not exist.")
        return False
    return True

def add_password_mainsail():
    password_file = "/etc/nginx/0-passwords.txt"
    nginx_conf = "/etc/nginx/sites-available/mainsail"
    auth_basic_line = '    auth_basic            "Minifab login";\n'
    auth_basic_user_file_line = f'    auth_basic_user_file  {password_file};\n'
    satisfy_any_block = (
        "    satisfy any;\n"
        "    allow 127.0.0.1;\n"
        "    deny  all;\n"
    )

    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "apache2-utils", "-y"], check=True)
    user_name = input("Enter the username for Mainsail: ").strip()
    password = input("Enter the password for Mainsail: ").strip()

    # Check if user already exists in the password file
    user_exists = False
    if os.path.exists(password_file):
        with open(password_file, "r") as f:
            for line in f:
                if line.startswith(user_name + ":"):
                    user_exists = True
                    break

    if user_exists:
        print(f"User '{user_name}' already exists in {password_file}.")
    else:
        if not os.path.exists(password_file):
            subprocess.run(["sudo", "htpasswd", "-b", "-c", password_file, user_name, password], check=True)
        else:
            subprocess.run(["sudo", "htpasswd", "-b", password_file, user_name, password], check=True)

    # Ensure auth_basic lines are present in nginx config
    # Read nginx config with sudo
    result = subprocess.run(
        ["sudo", "cat", nginx_conf],
        stdout=subprocess.PIPE,
        check=True,
        text=True
    )
    lines = result.stdout.splitlines(keepends=True)

    in_server = False
    server_brace_level = 0
    auth_basic_present = False
    auth_basic_user_file_present = False
    satisfy_any_present = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Detect start of server block
        if not in_server and stripped.startswith("server"):
            in_server = True
        if in_server and "{" in line:
            server_brace_level += line.count("{")
        if in_server and "}" in line:
            server_brace_level -= line.count("}")
        # Track if auth lines are present at server block level
        if in_server and server_brace_level == 1:
            if "auth_basic" in stripped and "auth_basic_user_file" not in stripped:
                auth_basic_present = True
            if "auth_basic_user_file" in stripped:
                auth_basic_user_file_present = True
            if "satisfy any" in stripped:
                satisfy_any_present = True
        # Before closing the top-level server block, insert if missing
        if in_server and server_brace_level == 0 and "}" in line:
            if not auth_basic_present:
                new_lines.append(auth_basic_line)
            if not auth_basic_user_file_present:
                new_lines.append(auth_basic_user_file_line)
            if not satisfy_any_present:
                new_lines.append(satisfy_any_block)
            in_server = False
            auth_basic_present = False
            auth_basic_user_file_present = False
            satisfy_any_present = False
        new_lines.append(line)

    # Write back using sudo tee
    new_content = "".join(new_lines)
    proc = subprocess.Popen(
        ["sudo", "tee", nginx_conf],
        stdin=subprocess.PIPE,
        text=True
    )

    proc.communicate(new_content)
    if proc.returncode != 0:
        print("Failed to write nginx config file.")
        return

    print("Nginx configuration updated. Reloading nginx...")
    subprocess.run(["sudo", "service", "nginx", "restart"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)

def menu(force_setup, clear_config, no_check, add_password):
    if add_password:
        add_password_mainsail()
        return
    # Check if setup has already been done by reading the status file
    if not check_username() and not no_check:
        return
    if not check_dir() and not no_check:
        return
    if os.path.exists(setup_status_file) and not force_setup:
        with open(setup_status_file, "r") as f:
            status = f.read().strip()
        if status == "setup_done":
            print("Setup has already been completed. Proceeding to update the configuration.")
            update_config(clear_config)
            return
        else:
            setup_config()
    else:
        setup_config()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true')
    parser.add_argument('-c', action='store_true')
    parser.add_argument('-nc', action='store_true')
    parser.add_argument('-p', action='store_true')
    args = parser.parse_args()

    menu(args.f, args.c, args.nc, args.p)
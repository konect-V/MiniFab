import re
import os
import time
import inspect
import subprocess
from datetime import datetime
from confswap import confswap

default_firmware = "idle"
logs = []
last_error_str = ""
current_toolhead = ""
firmware_available = []
forced = False

config_dir = "/home/minifab/printer_data/config/toolheads"
get_canbus_uuid_command = "/home/minifab/klippy-env/bin/python /home/minifab/klipper/scripts/canbus_query.py can0"

def get_forced():
    return forced

def get_current_firmware_available():
    return firmware_available

def get_current_toolhead():
    return current_toolhead

def get_last_error():
    return last_error_str

def get_logs():
    return logs

def log(msg, is_error):
    global last_error_str, logs
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    current_time = datetime.now()
    msg = msg.replace("\n", "")
    str = f"{current_time} : {calframe[1][3]} : {msg}"    
    logs.append(str)

    if is_error:
        last_error_str = str

def get_canbus_uuid():    
    try:
        # Execute command
        result = subprocess.run(get_canbus_uuid_command, shell=True, text=True, capture_output=True)
        
        # Check for errors
        if result.returncode != 0:
            log(result.stderr, True)
            return None
        
        # Extract UUIDs with regex
        uuids = re.findall(r"canbus_uuid=([a-fA-F0-9]+)", result.stdout)
        return uuids
    except Exception as e:
        log(e, True)
        return None


def extract_canbus_uuids():
    global firmware_available

    try:
        uuid_mapping = {}

        for folder in os.listdir(config_dir):
            folder_path = os.path.join(config_dir, folder)
            printer_cfg_path = os.path.join(folder_path, "printer.cfg")

            # Check if it's a directory and contains a printer.cfg file
            if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
                with open(printer_cfg_path, 'r') as file:
                    content = file.read()
                    
                    # Extract all canbus_uuid in the file
                    uuids = re.findall(r"canbus_uuid:\s*([a-fA-F0-9]+)", content)
                    
                    if uuids:
                        log(f"Found UUIDs in {folder}: {uuids}", False)
                        uuid_mapping[folder] = uuids
                        firmware_available.append(folder)
    except Exception as e:
        log(str(e), True)
    
    return uuid_mapping

def find_folder_by_uuid(uuid, uuid_mapping):
    for folder, uuids in uuid_mapping.items():
        if uuid in uuids:
            return folder
    log(f"UUID {uuid} not found in any folder", True)
    return None

def restart():
    command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.restart\",\"id\": 8463}' 0.0.0.0/printer/restart"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        log(result.stderr, True)
        return False
    return True

def firmware_restart():
    command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.firmware_restart\",\"id\": 8463}' 0.0.0.0/printer/firmware_restart"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        log(result.stderr, True)
        return False
    return True

def is_ready_or_startup():
    command = "curl 0.0.0.0/printer/info"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if '"state": "ready"' in result.stdout or '"state": "startup"' in result.stdout:
        if '"state": "ready"' in result.stdout:
            log("Printer is ready", False)
        else:
            log("Printer is starting up", False)
        return True
    log(result.stdout, False)
    return False

def firmware_swap(name):
    confswap(name)

def firmware_change(name):
    firmware_swap(name)
    restart()
    # wait restart
    time.sleep(5)
    ret = False
    while not ret:
        ret = firmware_restart()
        time.sleep(1)
    log(f"Firmware changed to : {name}", False) 

def autofirmware_daemon():
    global current_toolhead

    uuid_mapping = extract_canbus_uuids()

    # set at default_firmware first to avoid klipper error at startup
    current_toolhead = default_firmware
    firmware_change(current_toolhead)

    while True:
        if not forced:
            if not is_ready_or_startup() or current_toolhead == default_firmware:
                uuids = get_canbus_uuid()
                
                if uuids:
                    for uuid in uuids:
                        current_toolhead = find_folder_by_uuid(uuid, uuid_mapping)
                        firmware_change(current_toolhead)
        time.sleep(5)

def force_autofirmware(firmware):
    global forced, current_toolhead
    if firmware == "auto":
        forced = False
        current_toolhead = default_firmware
        firmware_change(default_firmware)
    else: 
        forced = True
        current_toolhead = firmware
        firmware_change(firmware)

import re
import os
import time
import inspect
import subprocess
import json
import logging
from datetime import datetime
from path_manager import PathManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/minifab/printer_data/logs/autofirmware.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('minifab.autofirmware')

# Initialize path manager
try:
    path_manager = PathManager('/home/minifab/MiniFab/src/config/paths.json')
except Exception as e:
    logger.error(f"Failed to initialize path manager: {e}")
    path_manager = None

logs = []
last_error_str = ""
current_toolhead = ""
firmware_available = []
forced = False

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
    log_str = f"{current_time} : {calframe[1][3]} : {msg}"    
    logs.append(log_str)
    
    if is_error:
        last_error_str = log_str
        logger.error(msg)
    else:
        logger.info(msg)

def get_canbus_uuid():
    # Command to execute
    command = "/home/minifab/klippy-env/bin/python /home/minifab/klipper/scripts/canbus_query.py can0"
    
    try:
        # Execute command
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        # Check for errors
        if result.returncode != 0:
            log(result.stderr, True)
            return None
        
        # Extract UUIDs with regex
        uuids = re.findall(r"canbus_uuid=([a-fA-F0-9]+)", result.stdout)
        return uuids
    except Exception as e:
        log(str(e), True)
        return None

def load_firmware_available():
    global firmware_available
    
    if path_manager:
        firmware_available = path_manager.get_available_toolheads()
    else:
        # Fallback to old method if path_manager failed to initialize
        firmware_available = []
        config_dir = "/home/minifab/printer_data/config/toolheads"
        
        for folder in os.listdir(config_dir):
            folder_path = os.path.join(config_dir, folder)
            printer_cfg_path = os.path.join(folder_path, "printer.cfg")
            
            if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
                firmware_available.append(folder)

def find_toolhead_by_uuid(uuid):
    if path_manager:
        return path_manager.find_toolhead_by_uuid(uuid)
    else:
        # Fallback to old method
        config_dir = "/home/minifab/printer_data/config/toolheads"
        for folder in os.listdir(config_dir):
            folder_path = os.path.join(config_dir, folder)
            printer_cfg_path = os.path.join(folder_path, "printer.cfg")
            
            if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
                try:
                    with open(printer_cfg_path, 'r') as file:
                        content = file.read()
                    
                    if f"canbus_uuid: {uuid}" in content:
                        return folder
                except Exception as e:
                    log(str(e), True)
        return None

def restart():
    command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.restart\",\"id\": 8463}' minifab.local/printer/restart"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        log(result.stderr, True)
        return None

def firmware_restart():
    command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.firmware_restart\",\"id\": 8463}' minifab.local/printer/firmware_restart"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        log(result.stderr, True)
        return None

def firmware_swap(toolhead):
    if path_manager:
        try:
            path_manager.switch_toolhead(toolhead)
            return True
        except Exception as e:
            log(f"Error in path_manager.switch_toolhead: {e}", True)
            # Fall back to confswap.py if path_manager fails
            
    # Old method as fallback
    command = f"python /home/minifab/MiniFab/src/scripts/confswap.py {toolhead}"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        log(result.stderr, True)
        return False
    return True

def firmware_change(toolhead):
    if firmware_swap(toolhead):
        restart()
        # wait restart
        time.sleep(5)
        firmware_restart()
        log(f"Firmware changed to : {toolhead}", False)
    else:
        log(f"Failed to swap firmware to {toolhead}", True)

def autofirmware_daemon():
    global current_toolhead
    
    # Load available firmwares
    load_firmware_available()
    
    # set at idle state first to avoid klipper error at startup
    current_toolhead = "iddle"
    firmware_change(current_toolhead)
    
    while True:
        if not forced:
            uuids = get_canbus_uuid()
            
            if uuids:
                for uuid in uuids:
                    found_toolhead = find_toolhead_by_uuid(uuid)
                    if found_toolhead and found_toolhead != current_toolhead:
                        current_toolhead = found_toolhead
                        firmware_change(current_toolhead)
            elif current_toolhead != "iddle":
                current_toolhead = "iddle"
                firmware_change(current_toolhead)
            time.sleep(5)

def force_autofirmware(firmware):
    global forced, current_toolhead
    if firmware == "auto":
        forced = False
        current_toolhead = "iddle"
        firmware_change("iddle")
    else: 
        forced = True
        current_toolhead = firmware
        firmware_change(firmware)

if __name__ == "__main__":
    autofirmware_daemon()
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

# Initialize constants
CONFIG_PATH = '/home/minifab/MiniFab/src/config/paths.json'
KLIPPER_RESTART_TIMEOUT = 10  # Seconds to wait for Klipper to restart
MAX_RETRY_ATTEMPTS = 3        # Maximum retry attempts for operations

# Initialize global variables
logs = []
last_error_str = ""
current_toolhead = ""
firmware_available = []
forced = False

# Initialize path manager
try:
    path_manager = PathManager(CONFIG_PATH)
    # Load firmware list from path manager
    firmware_available = path_manager.get_available_toolheads()
    logger.info(f"Path manager initialized with toolheads: {', '.join(firmware_available)}")
except FileNotFoundError as e:
    error_msg = f"Configuration file not found: {e}"
    logger.error(error_msg)
    path_manager = None
except Exception as e:
    error_msg = f"Failed to initialize path manager: {e}"
    logger.error(error_msg)
    path_manager = None


def get_forced():
    """Return whether toolhead selection is forced or automatic."""
    return forced


def get_current_firmware_available():
    """Return list of available firmware/toolhead options."""
    return firmware_available


def get_current_toolhead():
    """Return currently active toolhead."""
    return current_toolhead


def get_last_error():
    """Return the last error message."""
    return last_error_str


def get_logs():
    """Return all log messages."""
    return logs


def log(msg, is_error):
    """Add a message to the log with the current function name."""
    global last_error_str, logs
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    current_time = datetime.now()
    
    # Sanitize message
    msg = str(msg).replace("\n", " ")
    
    # Create log string
    log_str = f"{current_time} : {calframe[1][3]} : {msg}"    
    logs.append(log_str)
    
    # Update last error if this is an error message
    if is_error:
        last_error_str = log_str
        logger.error(msg)
    else:
        logger.info(msg)


def get_canbus_uuid():
    """Get the UUID of connected CAN devices.
    
    Returns:
        list: List of UUIDs or None if an error occurred
    """
    # Command to execute
    command = "/home/minifab/klippy-env/bin/python /home/minifab/klipper/scripts/canbus_query.py can0"
    
    try:
        # Execute command
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
        
        # Check for errors
        if result.returncode != 0:
            error_msg = f"Error querying CAN bus: {result.stderr}"
            log(error_msg, True)
            return None
        
        # Extract UUIDs with regex
        uuids = re.findall(r"canbus_uuid=([a-fA-F0-9]+)", result.stdout)
        
        if uuids:
            log(f"Found {len(uuids)} CAN devices: {', '.join(uuids)}", False)
        else:
            log("No CAN devices found", False)
            
        return uuids
        
    except subprocess.TimeoutExpired:
        log("Timeout while querying CAN bus", True)
        return None
    except Exception as e:
        log(f"Exception while querying CAN bus: {str(e)}", True)
        return None


def load_firmware_available():
    """Load the list of available firmware/toolheads."""
    global firmware_available
    
    if path_manager:
        try:
            # Get available toolheads from path manager
            firmware_available = path_manager.get_available_toolheads()
            log(f"Loaded {len(firmware_available)} available firmware options", False)
        except Exception as e:
            log(f"Error loading firmware options from path manager: {e}", True)
            # Fall back to directory scanning
            _load_firmware_from_directories()
    else:
        # No path manager, use directory scanning
        _load_firmware_from_directories()


def _load_firmware_from_directories():
    """Fallback method to load firmware options by scanning directories."""
    global firmware_available
    firmware_available = []
    config_dir = "/home/minifab/printer_data/config/toolheads"
    
    try:
        for folder in os.listdir(config_dir):
            folder_path = os.path.join(config_dir, folder)
            printer_cfg_path = os.path.join(folder_path, "printer.cfg")
            
            if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
                firmware_available.append(folder)
        
        log(f"Loaded {len(firmware_available)} available firmware options from directories", False)
    except Exception as e:
        log(f"Error scanning firmware directories: {e}", True)
        firmware_available = ["iddle"]  # Default to idle as fallback


def find_toolhead_by_uuid(uuid):
    """Find the toolhead associated with a CAN bus UUID.
    
    Args:
        uuid (str): The CAN bus UUID to match
        
    Returns:
        str: Toolhead name or None if not found
    """
    if not uuid:
        return None
        
    # Try using path manager first
    if path_manager:
        try:
            toolhead = path_manager.find_toolhead_by_uuid(uuid)
            if toolhead:
                log(f"Found toolhead {toolhead} for UUID {uuid} using path manager", False)
                return toolhead
        except Exception as e:
            log(f"Error finding toolhead by UUID using path manager: {e}", True)
    
    # Fall back to scanning config files
    try:
        config_dir = "/home/minifab/printer_data/config/toolheads"
        for folder in os.listdir(config_dir):
            folder_path = os.path.join(config_dir, folder)
            printer_cfg_path = os.path.join(folder_path, "printer.cfg")
            
            if os.path.isdir(folder_path) and os.path.isfile(printer_cfg_path):
                try:
                    with open(printer_cfg_path, 'r') as file:
                        content = file.read()
                    
                    if f"canbus_uuid: {uuid}" in content:
                        log(f"Found toolhead {folder} for UUID {uuid} by scanning config files", False)
                        return folder
                except Exception as e:
                    log(f"Error reading config file {printer_cfg_path}: {e}", True)
    except Exception as e:
        log(f"Error scanning config directories: {e}", True)
    
    log(f"No toolhead found for UUID {uuid}", False)
    return None


def is_klipper_ready():
    """Check if Klipper is ready and responding.
    
    Returns:
        bool: True if Klipper is ready, False otherwise
    """
    try:
        # Command to check Klipper status via Moonraker API
        command = "curl -s http://localhost:7125/printer/info"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=3)
        
        if result.returncode == 0 and "state" in result.stdout:
            # Parse JSON response
            response = json.loads(result.stdout)
            state = response.get("state", "")
            
            if state == "ready":
                return True
        
        return False
    except Exception:
        return False


def wait_for_klipper(timeout=KLIPPER_RESTART_TIMEOUT, interval=1):
    """Wait for Klipper to become ready.
    
    Args:
        timeout (int): Maximum time to wait in seconds
        interval (int): Check interval in seconds
        
    Returns:
        bool: True if Klipper became ready, False if timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_klipper_ready():
            log(f"Klipper is ready after {time.time() - start_time:.1f} seconds", False)
            return True
        
        time.sleep(interval)
    
    log(f"Timeout waiting for Klipper to become ready after {timeout} seconds", True)
    return False


def restart():
    """Restart Klipper service.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.restart\",\"id\": 8463}' minifab.local/printer/restart"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
        
        if result.returncode == 0:
            log("Klipper restart command sent successfully", False)
            return True
        else:
            log(f"Error restarting Klipper: {result.stderr}", True)
            return False
    except Exception as e:
        log(f"Exception restarting Klipper: {e}", True)
        return False


def firmware_restart():
    """Perform a firmware restart of Klipper.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        command = "curl -d '{\"jsonrpc\": \"2.0\",\"method\": \"printer.firmware_restart\",\"id\": 8463}' minifab.local/printer/firmware_restart"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
        
        if result.returncode == 0:
            log("Klipper firmware restart command sent successfully", False)
            return True
        else:
            log(f"Error sending firmware restart command: {result.stderr}", True)
            return False
    except Exception as e:
        log(f"Exception sending firmware restart command: {e}", True)
        return False


def firmware_swap(toolhead):
    """Switch Klipper configuration to a different toolhead.
    """
    # Try using path manager first
    if path_manager:
        try:
            success = path_manager.switch_toolhead(toolhead)
            if success:
                log(f"Successfully switched to toolhead {toolhead} using path manager", False)
                return True
            else:
                log(f"Failed to switch to toolhead {toolhead} using path manager", True)
                # Fall through to backup method
        except Exception as e:
            log(f"Error switching toolhead using path manager: {e}", True)
            # Fall through to backup method
    
    # Fallback: Use confswap.py script
    try:
        command = f"python /home/minifab/MiniFab/src/scripts/confswap.py {toolhead}"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
        
        if result.returncode == 0:
            log(f"Successfully switched to toolhead {toolhead} using confswap.py", False)
            return True
        else:
            log(f"Error running confswap.py: {result.stderr}", True)
            return False
    except Exception as e:
        log(f"Exception running confswap.py: {e}", True)
        return False


def firmware_change(toolhead):
    """Change firmware configuration and restart Klipper.
    
    Args:
        toolhead (str): Name of the toolhead to switch to
        
    Returns:
        bool: True if successful, False otherwise
    """
    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        log(f"Changing firmware to {toolhead} (attempt {attempt}/{MAX_RETRY_ATTEMPTS})", False)
        
        # Step 1: Swap firmware configuration
        if not firmware_swap(toolhead):
            log(f"Failed to swap firmware to {toolhead}", True)
            if attempt < MAX_RETRY_ATTEMPTS:
                time.sleep(2)
                continue
            return False
        
        # Step 2: Restart Klipper
        if not restart():
            log("Failed to restart Klipper", True)
            if attempt < MAX_RETRY_ATTEMPTS:
                time.sleep(2)
                continue
            return False
        
        # Step 3: Wait for Klipper to be ready
        if not wait_for_klipper(KLIPPER_RESTART_TIMEOUT):
            log("Klipper failed to restart within timeout", True)
            if attempt < MAX_RETRY_ATTEMPTS:
                time.sleep(2)
                continue
            return False
        
        # Step 4: Perform firmware restart
        if not firmware_restart():
            log("Failed to send firmware restart command", True)
            if attempt < MAX_RETRY_ATTEMPTS:
                time.sleep(2)
                continue
            return False
        
        # Step 5: Wait for Klipper to be ready again
        if not wait_for_klipper(KLIPPER_RESTART_TIMEOUT):
            log("Klipper failed to restart after firmware restart", True)
            if attempt < MAX_RETRY_ATTEMPTS:
                time.sleep(2)
                continue
            return False
        
        # Success!
        log(f"Successfully changed firmware to {toolhead}", False)
        return True
    
    # All attempts failed
    return False


def autofirmware_daemon():
    """Main daemon process for auto-detecting and switching toolheads."""
    global current_toolhead
    
    # Load available firmwares
    load_firmware_available()
    
    # Start in idle state to avoid Klipper errors
    current_toolhead = "iddle"
    firmware_change(current_toolhead)
    
    # Main monitoring loop
    while True:
        if not forced:
            uuids = get_canbus_uuid()
            
            if uuids:
                # Sort UUIDs for consistent behavior with multiple toolheads
                for uuid in sorted(uuids):
                    found_toolhead = find_toolhead_by_uuid(uuid)
                    if found_toolhead and found_toolhead != current_toolhead:
                        log(f"Detected new toolhead: {found_toolhead} (UUID: {uuid})", False)
                        current_toolhead = found_toolhead
                        firmware_change(current_toolhead)
                        break  # Only switch to the first detected toolhead
            elif current_toolhead != "iddle":
                log("No toolheads detected, switching to idle", False)
                current_toolhead = "iddle"
                firmware_change(current_toolhead)
        
        # Wait before next check
        time.sleep(5)


def force_autofirmware(firmware):
    """Force a specific firmware to be used.
    
    Args:
        firmware (str): Name of the firmware to force, or "auto" for automatic mode
    """
    global forced, current_toolhead
    
    if firmware == "auto":
        log("Switching to automatic toolhead detection", False)
        forced = False
        current_toolhead = "iddle"
        firmware_change("iddle")
    elif firmware in firmware_available:
        log(f"Forcing toolhead to {firmware}", False)
        forced = True
        current_toolhead = firmware
        firmware_change(firmware)
    else:
        log(f"Invalid firmware: {firmware}, must be one of: {', '.join(firmware_available)} or 'auto'", True)


if __name__ == "__main__":
    autofirmware_daemon()
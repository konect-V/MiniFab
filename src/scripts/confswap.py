#!/usr/bin/env python3
import os
import sys
import logging
import json
import argparse
from path_manager import PathManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/minifab/printer_data/logs/path_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('minifab.confswap')

def create_legacy_symlink(src_file, dest_file):
    """Legacy function to create symlinks for backward compatibility.
    
    Args:
        src_file (str): Source file path
        dest_file (str): Destination symlink path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if source file exists
        if not os.path.exists(src_file):
            logger.error(f"Source file does not exist: {src_file}")
            return False
            
        # Remove existing file or symlink
        if os.path.exists(dest_file):
            if os.path.isfile(dest_file):
                os.remove(dest_file)
            elif os.path.islink(dest_file):
                os.unlink(dest_file)
                
        # Create symlink
        os.symlink(src_file, dest_file)
        logger.info(f"Created symlink: {src_file} -> {dest_file}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create symlink {src_file} -> {dest_file}: {e}")
        return False


def legacy_confswap(config_name):
    """Legacy function to swap configurations without using path_manager.
    
    Args:
        config_name (str): Name of the toolhead configuration
        
    Returns:
        bool: True if successful, False otherwise
    """
    base_path = "/home/minifab/printer_data/config/toolheads"
    config_path = os.path.join(base_path, config_name)

    # Check if the folder exists
    if not os.path.isdir(config_path):
        logger.error(f"The folder '{config_path}' does not exist")
        return False

    # Create the symlinks
    printer_cfg = os.path.join(config_path, "printer.cfg")
    klipperscreen_cfg = os.path.join(config_path, "KlipperScreen.conf")
    
    success = create_legacy_symlink(printer_cfg, os.path.join(base_path, "printer.cfg"))
    if not success:
        return False
        
    # KlipperScreen config might not exist for all toolheads
    if os.path.exists(klipperscreen_cfg):
        success = create_legacy_symlink(klipperscreen_cfg, os.path.join(base_path, "KlipperScreen.conf"))
        if not success:
            return False
    
    return True


def main():
    """Main function for confswap script."""
    parser = argparse.ArgumentParser(description="Switch Klipper configuration to a specific toolhead")
    parser.add_argument("toolhead", help="Name of the toolhead configuration to switch to")
    parser.add_argument("--legacy", action="store_true", help="Use legacy mode without path_manager")
    parser.add_argument("--config", default="/home/minifab/MiniFab/src/config/paths.json", 
                         help="Path to the JSON configuration file")
    
    args = parser.parse_args()
    toolhead = args.toolhead
    
    # Display startup information
    logger.info(f"Starting confswap for toolhead: {toolhead}")
    
    if args.legacy:
        # Use legacy mode
        logger.info("Using legacy mode")
        if legacy_confswap(toolhead):
            logger.info(f"Successfully switched to toolhead: {toolhead} (legacy mode)")
            sys.exit(0)
        else:
            logger.error(f"Failed to switch to toolhead: {toolhead} (legacy mode)")
            sys.exit(1)
    
    # Use path_manager
    try:
        # Check if configuration file exists
        if not os.path.isfile(args.config):
            logger.error(f"Configuration file not found: {args.config}")
            
            # Fall back to legacy mode if configuration file is missing
            logger.info(f"Falling back to legacy mode")
            if legacy_confswap(toolhead):
                logger.info(f"Successfully switched to toolhead: {toolhead} (fallback legacy mode)")
                sys.exit(0)
            else:
                logger.error(f"Failed to switch to toolhead: {toolhead} (fallback legacy mode)")
                sys.exit(1)
        
        # Create path manager
        logger.info(f"Initializing path manager with config: {args.config}")
        path_manager = PathManager(args.config)
        
        # Check if toolhead exists
        available_toolheads = path_manager.get_available_toolheads()
        if toolhead not in available_toolheads:
            logger.error(f"Invalid toolhead: {toolhead}. Available toolheads: {', '.join(available_toolheads)}")
            sys.exit(1)
        
        # Switch to the specified toolhead
        logger.info(f"Switching to toolhead: {toolhead}")
        if path_manager.switch_toolhead(toolhead):
            logger.info(f"Successfully switched to toolhead: {toolhead}")
            sys.exit(0)
        else:
            logger.error(f"Failed to switch to toolhead: {toolhead}")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Failed to switch toolhead: {e}")
        
        # Fall back to legacy mode on error
        logger.info(f"Falling back to legacy mode after error")
        if legacy_confswap(toolhead):
            logger.info(f"Successfully switched to toolhead: {toolhead} (fallback legacy mode)")
            sys.exit(0)
        else:
            logger.error(f"Failed to switch to toolhead: {toolhead} (fallback legacy mode)")
            sys.exit(1)


if __name__ == "__main__":
    main()
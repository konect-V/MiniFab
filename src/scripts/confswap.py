#!/usr/bin/env python3
import os
import sys
import logging
import json
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

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python confswap.py <toolhead_name>")
        sys.exit(1)
    
    toolhead = sys.argv[1]
    
    try:
        # Path to the JSON configuration
        config_path = '/home/minifab/MiniFab/src/config/paths.json'
        
        # Create path manager
        path_manager = PathManager(config_path)
        
        # Check if toolhead exists
        available_toolheads = path_manager.get_available_toolheads()
        if toolhead not in available_toolheads:
            logger.error(f"Invalid toolhead: {toolhead}. Available toolheads: {', '.join(available_toolheads)}")
            sys.exit(1)
        
        # Switch to the specified toolhead
        path_manager.switch_toolhead(toolhead)
        logger.info(f"Successfully switched to toolhead: {toolhead}")
        
    except Exception as e:
        logger.error(f"Failed to switch toolhead: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
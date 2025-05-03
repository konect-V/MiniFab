import json
import os
import shutil
import logging
from typing import Dict, List, Optional

class PathManager:
    def __init__(self, config_path: str):
        """
        Initialize the PathManager with a path to the JSON configuration file.
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = logging.getLogger('minifab.path_manager')
    
    def _load_config(self) -> Dict:
        """Load the configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
    
    def get_base_path(self, key: str) -> str:
        """Get a base path by key."""
        if key not in self.config['base_paths']:
            raise KeyError(f"Base path '{key}' not found in configuration")
        return self.config['base_paths'][key]
    
    def get_toolhead_path(self, toolhead: str, path_key: str) -> str:
        """Get a specific path for a toolhead."""
        if toolhead not in self.config['toolheads']:
            raise KeyError(f"Toolhead '{toolhead}' not found in configuration")
        
        toolhead_config = self.config['toolheads'][toolhead]
        if path_key not in toolhead_config:
            raise KeyError(f"Path key '{path_key}' not found for toolhead '{toolhead}'")
        
        path = toolhead_config[path_key]
        if path.startswith('/'):
            return path
        
        # Handle relative paths
        if path_key == 'printer_cfg' or path_key == 'klipperscreen_cfg':
            return os.path.join(self.get_base_path('config'), path)
        
        return path
    
    def get_toolhead_canbus_uuid(self, toolhead: str) -> str:
        """Get the CAN bus UUID for a specific toolhead."""
        return self.get_toolhead_path(toolhead, 'canbus_uuid')
    
    def get_available_toolheads(self) -> List[str]:
        """Get a list of all available toolheads."""
        return list(self.config['toolheads'].keys())
    
    def find_toolhead_by_uuid(self, uuid: str) -> Optional[str]:
        """Find a toolhead name by its CAN bus UUID."""
        for toolhead, config in self.config['toolheads'].items():
            if config.get('canbus_uuid') == uuid:
                return toolhead
        return None
    
    def create_symlink(self, src_file: str, dest_file: str) -> None:
        """Create a symlink, handling existing files."""
        try:
            if os.path.exists(dest_file):
                if os.path.isfile(dest_file):
                    os.remove(dest_file)
            if os.path.islink(dest_file):
                os.unlink(dest_file)
            os.symlink(src_file, dest_file)
            self.logger.info(f"Symlink created: {src_file} -> {dest_file}")
        except Exception as e:
            self.logger.error(f"Error creating symlink {src_file}: {e}")
            raise
    
    def switch_toolhead(self, toolhead: str) -> None:
        """Switch to a specific toolhead configuration."""
        if toolhead not in self.config['toolheads']:
            raise KeyError(f"Toolhead '{toolhead}' not found in configuration")
        
        toolhead_dir = os.path.join(self.get_base_path('toolheads'), toolhead)
        if not os.path.isdir(toolhead_dir):
            raise FileNotFoundError(f"Toolhead directory '{toolhead_dir}' not found")
        
        # Create the symlinks for printer.cfg and KlipperScreen.conf
        printer_cfg = self.get_toolhead_path(toolhead, 'printer_cfg')
        klipperscreen_cfg = self.get_toolhead_path(toolhead, 'klipperscreen_cfg')
        
        self.create_symlink(
            printer_cfg,
            os.path.join(self.get_base_path('toolheads'), 'printer.cfg')
        )
        
        self.create_symlink(
            klipperscreen_cfg,
            os.path.join(self.get_base_path('toolheads'), 'KlipperScreen.conf')
        )
        
        self.logger.info(f"Switched to toolhead '{toolhead}'")
        return True
import json
import os
import shutil
import logging
from typing import Dict, List, Optional

class PathManager:
    def __init__(self, config_path: str):
        """
        Initialize the PathManager with a path to the JSON configuration file.
        
        Args:
            config_path: Path to the JSON configuration file
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        self.config_path = config_path
        self.logger = self._setup_logger()
        self.config = self._load_config()
        self._validate_config()
    
    def _setup_logger(self):
        """Set up logger for path manager."""
        logger = logging.getLogger('minifab.path_manager')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_config(self) -> Dict:
        """Load the configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.logger.info(f"Successfully loaded configuration from {self.config_path}")
                return config
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON configuration: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Failed to load config from {self.config_path}: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _validate_config(self):
        """Validate the loaded configuration."""
        required_keys = ['base_paths', 'toolheads', 'common_configs']
        for key in required_keys:
            if key not in self.config:
                error_msg = f"Missing required key '{key}' in configuration"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
        
        # Validate base paths
        if not isinstance(self.config['base_paths'], dict):
            raise ValueError("'base_paths' must be a dictionary")
        
        # Validate toolheads
        if not isinstance(self.config['toolheads'], dict) or not self.config['toolheads']:
            raise ValueError("'toolheads' must be a non-empty dictionary")
        
        for toolhead, toolhead_config in self.config['toolheads'].items():
            required_toolhead_keys = ['printer_cfg', 'klipperscreen_cfg']
            for key in required_toolhead_keys:
                if key not in toolhead_config:
                    raise ValueError(f"Missing required key '{key}' for toolhead '{toolhead}'")
        
        self.logger.info("Configuration validation successful")
    
    def get_base_path(self, key: str) -> str:
        """Get a base path by key."""
        if key not in self.config['base_paths']:
            error_msg = f"Base path '{key}' not found in configuration"
            self.logger.error(error_msg)
            raise KeyError(error_msg)
        return self.config['base_paths'][key]
    
    def get_toolhead_path(self, toolhead: str, path_key: str) -> str:
        """Get a specific path for a toolhead."""
        if toolhead not in self.config['toolheads']:
            error_msg = f"Toolhead '{toolhead}' not found in configuration"
            self.logger.error(error_msg)
            raise KeyError(error_msg)
        
        toolhead_config = self.config['toolheads'][toolhead]
        if path_key not in toolhead_config:
            error_msg = f"Path key '{path_key}' not found for toolhead '{toolhead}'"
            self.logger.error(error_msg)
            raise KeyError(error_msg)
        
        path = toolhead_config[path_key]
        if path.startswith('/'):
            # Absolute path
            return path
        
        # Handle relative paths based on the type of configuration
        if path_key == 'printer_cfg' or path_key == 'klipperscreen_cfg':
            return os.path.join(self.get_base_path('config'), path)
        elif path_key == 'canbus_uuid':
            # UUID is not a path
            return path
        elif path_key == 'configs':
            # This is a list of config files
            return [os.path.join(self.get_base_path('config'), 'toolheads', toolhead, config) 
                    for config in path]
        else:
            # Default case: prepend the toolhead directory
            return os.path.join(self.get_base_path('config'), 'toolheads', toolhead, path)
    
    def get_toolhead_canbus_uuid(self, toolhead: str) -> str:
        """Get the CAN bus UUID for a specific toolhead."""
        return self.get_toolhead_path(toolhead, 'canbus_uuid')
    
    def get_available_toolheads(self) -> List[str]:
        """Get a list of all available toolheads."""
        return list(self.config['toolheads'].keys())
    
    def find_toolhead_by_uuid(self, uuid: str) -> Optional[str]:
        """Find a toolhead name by its CAN bus UUID."""
        if not uuid:
            return None
            
        for toolhead, config in self.config['toolheads'].items():
            if config.get('canbus_uuid') == uuid:
                return toolhead
        return None
    
    def create_symlink(self, src_file: str, dest_file: str) -> None:
        """Create a symlink, handling existing files."""
        try:
            # Verify source file exists
            if not os.path.exists(src_file):
                error_msg = f"Source file does not exist: {src_file}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            # Handle existing destination
            if os.path.exists(dest_file):
                if os.path.isfile(dest_file) and not os.path.islink(dest_file):
                    os.remove(dest_file)
                    self.logger.info(f"Removed existing file: {dest_file}")
                elif os.path.isdir(dest_file):
                    shutil.rmtree(dest_file)
                    self.logger.info(f"Removed existing directory: {dest_file}")
            
            # Remove existing symlink
            if os.path.islink(dest_file):
                os.unlink(dest_file)
                self.logger.info(f"Removed existing symlink: {dest_file}")
            
            # Create parent directory if needed
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
                self.logger.info(f"Created directory: {dest_dir}")
            
            # Create the symlink
            os.symlink(src_file, dest_file)
            self.logger.info(f"Created symlink: {src_file} -> {dest_file}")
        
        except FileNotFoundError as e:
            self.logger.error(f"Source file not found: {e}")
            raise
        except PermissionError as e:
            self.logger.error(f"Permission error creating symlink: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error creating symlink {src_file} -> {dest_file}: {e}")
            raise
    
    def switch_toolhead(self, toolhead: str) -> bool:
        """Switch to a specific toolhead configuration."""
        try:
            if toolhead not in self.config['toolheads']:
                error_msg = f"Toolhead '{toolhead}' not found in configuration"
                self.logger.error(error_msg)
                raise KeyError(error_msg)
            
            # Get toolhead directory path
            toolhead_dir = os.path.join(self.get_base_path('config'), f"toolheads/{toolhead}")
            if not os.path.isdir(toolhead_dir):
                error_msg = f"Toolhead directory not found: {toolhead_dir}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            # Get configuration file paths
            printer_cfg = self.get_toolhead_path(toolhead, 'printer_cfg')
            klipperscreen_cfg = self.get_toolhead_path(toolhead, 'klipperscreen_cfg')
            
            # Verify config files exist
            if not os.path.exists(printer_cfg):
                error_msg = f"Printer configuration file not found: {printer_cfg}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            # Create symlinks
            self.create_symlink(
                printer_cfg,
                os.path.join(self.get_base_path('toolheads'), 'printer.cfg')
            )
            
            # KlipperScreen config might not exist for all toolheads
            if os.path.exists(klipperscreen_cfg):
                self.create_symlink(
                    klipperscreen_cfg,
                    os.path.join(self.get_base_path('toolheads'), 'KlipperScreen.conf')
                )
            else:
                self.logger.warning(f"KlipperScreen config not found for {toolhead}: {klipperscreen_cfg}")
            
            self.logger.info(f"Successfully switched to toolhead '{toolhead}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to switch toolhead to '{toolhead}': {e}")
            return False
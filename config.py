import os
import logging
from configparser import ConfigParser

def ensure_utf8_config(file_path: str) -> None:
    """Ensures the config.ini file is UTF-8 encoded."""
    with open(file_path, 'r', encoding='ascii', errors='ignore') as f:
        content = f.read()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_config() -> ConfigParser:
    """Loads the configuration from config.ini."""
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, 'config.ini')
    ensure_utf8_config(config_path)
    
    config = ConfigParser(interpolation=None)
    config.read(config_path, encoding='utf-8')
    
    return config

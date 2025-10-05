from pathlib import Path
import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    
    # Resolve path relative to project root
    BASE_DIR = Path(__file__).resolve().parent.parent  # utils/ -> project root
    full_path = BASE_DIR / config_path
    
    with open(config_path, "r") as file:
        config=yaml.safe_load(file)
    print(config)
    
    return config    




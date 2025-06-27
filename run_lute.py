import os
import yaml
import subprocess
from pathlib import Path
import tempfile

def expand_and_resolve(path_str: str) -> Path:
    """Expand ~ and make absolute."""
    return Path(path_str).expanduser().resolve()

# Load config.yml from the same directory as this script
base_dir = Path(__file__).resolve().parent
config_file = base_dir / "config.yml"

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

# Resolve paths and create folders if needed
for key in ["DATAPATH", "BACKUP_PATH"]:
    if key in config:
        abs_path = expand_and_resolve(config[key])
        abs_path.mkdir(parents=True, exist_ok=True)
        config[key] = str(abs_path)

# Write updated config to a temp file
with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as tmp:
    yaml.dump(config, tmp)
    tmp_path = tmp.name

# Run Lute with the resolved config
subprocess.run(["python", "-m", "lute.main", "--port", "9876", "--config", tmp_path])

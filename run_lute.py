import os
import yaml
import subprocess
from pathlib import Path
import tempfile

# Load original relative config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

base_dir = Path(__file__).resolve().parent

# Convert paths to absolute
if "DATAPATH" in config:
    config["DATAPATH"] = str((base_dir / config["DATAPATH"]).resolve())

if "BACKUP_PATH" in config:
    config["BACKUP_PATH"] = str((base_dir / config["BACKUP_PATH"]).resolve())

# Save temp config
with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as tmp:
    yaml.dump(config, tmp)
    tmp_path = tmp.name

# Run lute with temp config
subprocess.run(["python", "-m", "lute.main", "--port", "9876", "--config", tmp_path])

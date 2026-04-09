import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".sshconnect.json"
SSH_CONFIG_FILE = Path.home() / ".ssh" / "config"
ASKPASS_SCRIPT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "askpass.py")

START_MARKER = "# --- SSHCONNECT Start ---"
END_MARKER = "# --- SSHCONNECT End ---"
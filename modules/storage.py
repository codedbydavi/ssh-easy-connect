import os
import json
import re
from modules.constants import CONFIG_FILE, SSH_CONFIG_FILE, START_MARKER, END_MARKER

def load_data():
    """Load data from the config file. Returns an empty dict if the file doesn't exist."""
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    
def save_data(data):
    """Save data to the config file and update SSH config."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
    os.chmod(CONFIG_FILE, 0o600)
    update_ssh_config(data.get("servers", []))

def update_ssh_config(servers):
    """Update the user's SSH config file with the managed servers."""
    SSH_CONFIG_FILE.parent.mkdir(exist_ok=True, mode=0o700)
    os.chmod(SSH_CONFIG_FILE.parent, 0o700)

    content = SSH_CONFIG_FILE.read_text() if SSH_CONFIG_FILE.exists() else ""
    blocks = [START_MARKER]
    for s in servers:
        alias = s["name"].replace(" ", "_")
        blocks.extend([
            f"Host {alias}",
            f"    HostName {s['host']}",
            f"    User {s['user']}",
            f"    Port {s['port']}",
            ""
        ])
    blocks.append(END_MARKER)
    managed_section = "\n".join(blocks)

    if START_MARKER in content and END_MARKER in content:
        pattern = f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}"
        new_content = re.sub(
            pattern,
            managed_section,
            content,
            flags=re.DOTALL
        )
    else:
        new_content = content.strip() + "\n\n" + managed_section if content.strip() else managed_section
    
    SSH_CONFIG_FILE.write_text(new_content)
    os.chmod(SSH_CONFIG_FILE, 0o600)
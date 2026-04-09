import os
import subprocess
import threading
import stat
import curses
from modules.constants import ASKPASS_SCRIPT
from modules.utils import reset_terminal, flush_input
from modules.security import get_cipher

ping_status = {}

def run_pings_once(servers):
    """Run ping checks for all servers once and update the global ping_status dictionary."""
    global ping_status
    for server in servers:
        ping_status[server["host"]] = "⚪️"

    def worker():
        """Worker thread to perform ping checks without blocking the main UI."""
        for server in servers:
            res = subprocess.run(["ping", "-c", "1", "-W", "1", server["host"]], capture_output=True, stdout=subprocess.DEVNULL)
            ping_status[server["host"]] = "🟢" if res.returncode == 0 else "🔴"
        try: curses.ungetch(0)  # Trigger screen refresh
        except: pass  # Ignore if curses is not initialized

    threading.Thread(target=worker, daemon=True).start()

def connect_to_server(stdscr, conn, mode="ssh", command=None):
    """mode can be 'ssh', 'mc', or 'cmd' (for running a command)"""
    cipher = get_cipher()
    pw = cipher.decrypt(conn["password"].encode()).decode() if conn.get("password") else ""
    alias = conn["name"].replace(" ", "_")

    stdscr.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    reset_terminal()
    os.system("clear")

    env = os.environ.copy()
    env["TERM"] = "xterm"

    if mode == "mc":
        if pw:
            with open(ASKPASS_SCRIPT, "w") as f:
                f.write(f"#!/bin/bash\necho '{pw}'")
            os.chmod(ASKPASS_SCRIPT, stat.S_IRWXU)
            env.update({"SSH_ASKPASS": ASKPASS_SCRIPT, "DISPLAY": ":0", "SSH_ASKPASS_REQUIRE": "force"})
            cmd = ["setsid", "mc", "-u", ".", f"sh://{conn['user']}@{conn['host']}:{conn['port']}/"]
        else:
            cmd = ["mc", "-u", ".", f"sh://{alias}/"]
    elif mode == "cmd":
        has_sshpass = subprocess.run(["which", "sshpass"], capture_output=True).returncode == 0
        if pw and has_sshpass:
            env["SSHPASS"] = pw
            cmd = ["sshpass", "-e", "ssh", alias, command]
        else:
            cmd = ["ssh", alias, command]
    else:
        has_sshpass = subprocess.run(["which", "sshpass"], capture_output=True).returncode == 0
        if pw and has_sshpass:
            env["SSHPASS"] = pw
            cmd = ["sshpass", "-e", "ssh", alias]
        else:
            cmd = ["ssh", alias]
        
    try:
        if mode == "cmd":
            print(f"Executando: {command}\n")
            subprocess.run(cmd, env=env)
            input("\n[Pressione ENTER para voltar]")
        else:
            subprocess.run(cmd, env=env)
    finally:
        if os.path.exists(ASKPASS_SCRIPT):
            os.remove(ASKPASS_SCRIPT)
    
    reset_terminal()
    curses.reset_shell_mode()
    curses.cbreak()
    curses.noecho()
    stdscr.clear()
    curses.curs_set(0)
    stdscr.keypad(True)
    flush_input()

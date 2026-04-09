import curses
from modules.utils import flush_input
from modules.security import get_cipher
from modules.storage import save_data
from modules.network import ping_status

def get_input(stdscr, prompt, default="", is_password=False):
    """Display a prompt at the bottom of the screen and captures user input. If is_password is True, input will be hidden."""
    flush_input()
    curses.curs_set(1)
    curses.echo()
    if is_password: curses.noecho()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h - 3, 2, " " * (w-4))
    stdscr.addstr(h - 3, 2, f" {prompt} [{default}] > ")
    input_str = stdscr.getstr().decode('utf-8').strip()
    curses.noecho()
    curses.curs_set(0)
    return input_str if input_str else default

def select_group(stdscr, data):
    """Displays existing groups and allows the user to select one or create a new group."""
    servers = data.get("servers", [])
    existing_groups = sorted(list(set(s.get("group", "General") for s in servers)))
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.attron(curses.color_pair(4))
    stdscr.border()
    stdscr.attroff(curses.color_pair(4))
    stdscr.addstr(2, 4, "Choose an existing group or create a new one:", curses.A_BOLD)
    for i, g in enumerate(existing_groups):
        stdscr.addstr(4 + i, 6, f"{i}) {g}")
    next_idx = len(existing_groups)
    stdscr.addstr(4 + next_idx, 6, f"{next_idx}) [ NEW GROUP ]")
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    ch = stdscr.getstr(4 + next_idx + 2, 6).decode('utf-8').strip()
    curses.noecho()
    curses.curs_set(0)
    try:
        idx = int(ch)
        if idx < next_idx: return existing_groups[idx]
    except: pass
    return get_input(stdscr, "New group name", "General")

def add_edit_conn(stdscr, data, index=None):
    """If index is None, adds a new connection. Otherwise, edits the connection at the given index."""
    servers = data.get("servers", [])
    is_edit = index is not None
    conn = servers[index] if is_edit else {"name": "", "user": "root", "host": "", "port": 22, "password": "", "group": "Geral"}
    
    name = get_input(stdscr, "Name", conn["name"])
    user = get_input(stdscr, "User", conn["user"])
    host = get_input(stdscr, "Host/IP", conn["host"])
    port = get_input(stdscr, "Port", str(conn["port"]))
    group = select_group(stdscr, data)
    pw = get_input(stdscr, "Password (leave blank to keep current)", "", is_password=True)
    
    cipher = get_cipher()
    enc_pw = cipher.encrypt(pw.encode()).decode() if pw else conn.get("password", "")
    new_c = {"name": name, "user": user, "host": host, "port": int(port) if port.isdigit() else 22, "password": enc_pw, "group": group}
    
    if is_edit: servers[index] = new_c
    else: servers.append(new_c)
    data["servers"] = servers
    save_data(data)

def draw_menu(stdscr, servers, current_row, search_query, active_group):
    """Renders the main TUI menu with the list of servers, search bar, and footer instructions."""
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.attron(curses.color_pair(4))
    stdscr.border()
    stdscr.attroff(curses.color_pair(4))
    
    title = f" 🖥️  SSH CONNECT ULTIMATE v2 | Group: {active_group} "
    stdscr.addstr(0, (w // 2) - (len(title) // 2), title, curses.color_pair(1) | curses.A_BOLD)
    
    if search_query:
        stdscr.addstr(1, 4, f"🔍 Search: {search_query}", curses.color_pair(3))
        
    stdscr.addstr(2, 4, f"{'ID':<4} {'ST':<3} {'NAME':<20} {'CONNECTION':<25} {'GROUP':<10}", curses.A_UNDERLINE)
    
    for idx, conn in enumerate(servers):
        if idx >= h - 6: break
        st = ping_status.get(conn['host'], "⚪")
        pi = "🔑" if conn.get("password") else "  "
        line = f" {idx:2d}  │ {st} │ {conn['name'][:19]:<20} │ {conn['user']}@{conn['host'][:15]:<15} {pi} │ {conn.get('group','General')[:9]}"
        if idx == current_row:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(4 + idx, 2, f"  {line}  ")
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(4 + idx, 2, f"  {line}  ")
            
    ft = " [ENTER] SSH  [m] MC  [c] Cmd  [g] Group  [/] Search  [a] Add  [e] Edit  [d] Del  [q] Quit "
    stdscr.addstr(h - 1, max(0, (w // 2) - (len(ft) // 2)), ft[:w-2], curses.color_pair(3))
    stdscr.refresh()

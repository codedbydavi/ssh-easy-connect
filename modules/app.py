import curses
from modules.storage import load_data, save_data
from modules.network import run_pings_once, connect_to_server
from modules.ui import draw_menu, add_edit_conn, get_input

def main_tui(stdscr):
    """Main entry point for the curses-based TUI application."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    
    curses.curs_set(0)
    current_row = 0
    search_query = ""
    active_group = "All"
    
    data = load_data()
    run_pings_once(data.get("servers", []))

    while True:
        all_servers = data.get("servers", [])
        groups = ["All"] + list(sorted(set(s.get("group", "General") for s in all_servers)))
        
        # Filtragem
        servers = [s for s in all_servers if (active_group == "All" or s.get("group", "General") == active_group)]
        if search_query:
            servers = [s for s in servers if search_query.lower() in s["name"].lower() or search_query in s["host"]]
        
        current_row = max(0, min(current_row, len(servers) - 1))
        draw_menu(stdscr, servers, current_row, search_query, active_group)
        
        stdscr.timeout(-1)
        key = stdscr.getch()
        
        if key == -1 or key == 0: continue

        if key == curses.KEY_UP and current_row > 0: current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(servers) - 1: current_row += 1
        elif key in [ord('\n'), ord('m'), ord('c')] and servers:
            if key == ord('\n'): connect_to_server(stdscr, servers[current_row], "ssh")
            elif key == ord('m'): connect_to_server(stdscr, servers[current_row], "mc")
            elif key == ord('c'):
                snips = data.get("snippets", [])
                if not snips:
                    stdscr.addstr(curses.LINES-2, 2, "No snippets.", curses.color_pair(3))
                    stdscr.getch()
                    continue
                
                stdscr.clear()
                stdscr.addstr(1, 2, "Snippet:", curses.A_BOLD)
                for i, s in enumerate(snips):
                    stdscr.addstr(3+i, 4, f"{i}) {s['name']}")
                
                stdscr.refresh()
                curses.echo()
                curses.curs_set(1)
                ch = stdscr.getch()
                curses.noecho()
                curses.curs_set(0)
                try:
                    connect_to_server(stdscr, servers[current_row], "cmd", snips[int(chr(ch))]["command"])
                except: pass
            
            data = load_data()
            run_pings_once(data.get("servers", []))
            
        elif key == ord('a'): 
            add_edit_conn(stdscr, data)
            data = load_data()
            run_pings_once(data.get("servers", []))
        elif key == ord('e') and servers:
            ridx = all_servers.index(servers[current_row])
            add_edit_conn(stdscr, data, ridx)
            data = load_data()
            run_pings_once(data.get("servers", []))
        elif key == ord('d') and servers:
            stdscr.addstr(curses.LINES-2, 2, "Confirm? (y/n)", curses.color_pair(3))
            if stdscr.getch() == ord('y'):
                ridx = all_servers.index(servers[current_row])
                all_servers.pop(ridx)
                data["servers"] = all_servers
                save_data(data)
                data = load_data()
        elif key == ord('g'):
            idx = groups.index(active_group)
            active_group = groups[(idx + 1) % len(groups)]
            current_row = 0
        elif key == ord('/'):
            search_query = get_input(stdscr, "Search")
            current_row = 0
        elif key == ord('q'): break

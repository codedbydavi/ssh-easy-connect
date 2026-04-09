import os
import sys
import curses
import termios

def flush_input():
    """Flush any pending input from the terminal."""
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        try: curses.flushinp()  # Flush curses input buffer if in curses mode
        except: pass
    except: pass

def reset_terminal():
    """Reset terminal settings to sane defaults."""
    modes = ["?1000", "?1001", "?1002", "?1003", "?1005", "?1006", "?1015", "?1049"]  # Disable mouse modes
    try:
        os.write(sys.stdout.fileno(), "".join([f"\x1b[{m}l" for m in modes]).encode())
        os.write(sys.stdout.fileno(), b"\033[0m\033[?25h")  # Reset attributes and show cursor]")
    except: pass
    flush_input()
    os.system('stty sane')  # Reset terminal settings
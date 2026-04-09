import curses
import os
from modules.security import init_crypto
from modules.storage import save_data
from modules.app import main_tui


if __name__ == "__main__":
    # Initialize the crypto system before entering curses mode
    init_crypto(save_data)

    try:
        curses.wrapper(main_tui)
    except KeyboardInterrupt:
        pass
    finally:
        os.system('stty sane')  # Reset terminal settings on exit
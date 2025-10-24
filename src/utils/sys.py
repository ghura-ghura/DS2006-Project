from sys import exit as sys_exit
from typing import Callable
from time import sleep
import sys
import os

def flush_input() -> None:
    flush_input_windows() if os.name == 'nt' else flush_input_unix()

def flush_input_windows(max_attempts: int = 10) -> None:
    from msvcrt import getch, kbhit

    for _ in range(max_attempts):
        if not kbhit():
            break
        _ = getch()

def flush_input_unix() -> None:
    import termios
    import tty
    
    try:
        # Get terminal settings
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        # Set terminal to raw mode temporarily
        tty.setraw(sys.stdin.fileno())
        
        # Flush any pending input
        import select
        while select.select([sys.stdin], [], [], 0.1)[0]:
            sys.stdin.read(1)
            
    except (ImportError, OSError):
        pass
    finally:
        try:
            # Restore terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (NameError, OSError):
            pass

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def quit(set_exiting: Callable[[bool], None], force_exit: bool = False) -> None:
    set_exiting(True)
    flush_input()
    print("\nExiting...")
    sleep(1)
    if force_exit:
        sys_exit()
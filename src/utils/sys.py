from os import system as os_system
from sys import exit as sys_exit
from typing import Callable
from time import sleep

def flush_input_windows(max_attempts: int = 10) -> None:
        from msvcrt import getch, kbhit

        for _ in range(max_attempts):
            if not kbhit():
                break
            _ = getch()

def clear_screen_windows() -> None:
    os_system('cls')

def quit(set_exiting: Callable[[bool], None], force_exit: bool = False) -> None:
    set_exiting(True)
    flush_input_windows()
    print("\nExiting...")
    sleep(1)
    if force_exit:
        sys_exit()
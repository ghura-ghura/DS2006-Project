from os import system as os_system

def flush_input_windows(max_attempts: int = 10) -> None:
        from msvcrt import getch, kbhit

        for _ in range(max_attempts):
            if not kbhit():
                break
            _ = getch()

def clear_screen_windows() -> None:
    os_system('cls')
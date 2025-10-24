from typing import Callable
import sys
import os

class KeyHandler:
    def __init__(self) -> None:
        self.is_windows = os.name == 'nt'
        if not self.is_windows:
            import tty, termios
            self.tty = tty
            self.termios = termios

    def get_key(self) -> str | None:
        if self.is_windows:
            return self.get_key_windows()
        else:
            return self.get_key_unix()

    def get_key_windows(self) -> str | None:
        from msvcrt import kbhit, getch
        
        if not self.is_key_pressed_windows(kbhit):
            return
        
        key = getch()

        arrow_keys_pressed = self.arrow_keys_pressed_windows(key)
        w_s_keys_pressed = self.w_s_keys_pressed_windows(key)

        if arrow_keys_pressed or w_s_keys_pressed:
            if arrow_keys_pressed:
                key = getch()
            
            match key:
                case b'H' | b'w':
                    return 'w'
                case b'P' | b's':
                    return 's'
        elif self.is_enter_key_windows(key):
            return '\r'
        elif self.is_escape_key_windows(key):
            return '\x1b'

        return key.decode(encoding="ascii", errors="ignore")

    def get_key_unix(self) -> str | None:
        fd = sys.stdin.fileno()
        old_settings = self.termios.tcgetattr(fd)
        
        try:
            self.tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            if ch == '\x1b':  # Escape sequence
                # Check if it's a single Esc or part of arrow key sequence
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        match ch3:
                            case 'A':  # Up arrow
                                return 'w'
                            case 'B':  # Down arrow
                                return 's'
                else:
                    # Single Esc key
                    return '\x1b'
            elif ch == '\r':  # Enter
                return '\r'
            elif ch in ['w', 'W', 's', 'S']:  # W/S keys
                return ch.lower()
            else:
                return ch
                
        finally:
            self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
        
    def arrow_keys_pressed_windows(self, key: str) -> bool:
        return key == b'\xe0'

    def is_key_pressed_windows(self, kbhit: Callable[[], bool]) -> bool:
        return kbhit()

    def is_enter_key_windows(self, key: str) -> bool:
        return key == b'\r'

    def is_escape_key_windows(self, key: str) -> bool:
        return key == b'\x1b'

    def w_s_keys_pressed_windows(self, key: str) -> bool:
        return key in [b'W', b'w', b'S', b's']
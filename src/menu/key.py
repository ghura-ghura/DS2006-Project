from msvcrt import kbhit, getch
from typing import Callable

class KeyHandler:
    def __init__(self) -> None:
        pass

    def get_key_windows(self) -> str | None:
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
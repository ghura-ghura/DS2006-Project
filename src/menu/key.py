from typing import Callable
import sys
import os
from readchar import readkey, key # To handle cross-platform input 

class KeyHandler:
    def __init__(self) -> None: 
        # We don't need a specific setup for OS using cross-plattform read instead
        pass

    def get_key(self) -> str | None:
        # Block until a key is pressed and normalize menu and make sure to treat w and "uparrow" and s"downarrow"
        k = readkey() # crossplattform read 

        # Map arrows and WS to 'w' and 's' 
        if k in (key.UP, 'w', 'W'):
            return 'w'
        if k in (key.DOWN, 's', 'S'):
            return 's'

        # Enter/Escape mapping
        if k in (key.ENTER, '\r', '\n'):
            return '\r'
        if k in (key.ESC, '\x1b'):
            return '\x1b'
        # Fallback to return the raw key if the others aren't fulfilled
        return k 

from pygame import event as pygame_event, Rect
from typing import Callable

ColorFunction = Callable[[int], tuple[int, int, int]]

SelectorFunction = Callable[[int], None]

PyGameEventFunction = Callable[[pygame_event.Event], bool]

SetBackRectFunction = Callable[[Rect], None]
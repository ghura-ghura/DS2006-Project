from typing import Callable

ColorFunction = Callable[[int], tuple[int, int, int]]

SelectorFunction = Callable[[int], None]

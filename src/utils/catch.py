from typing import Callable, Type
from src.types.main import T, E

def try_catch(callback: Callable[[], T], exception: type[E], err_msg: str = "", include_exception: bool = False) -> T | None:
    try:
        return callback()
    except exception as e:
        print(f"{e.__class__.__name__}: {err_msg}" if include_exception else err_msg)
        return None
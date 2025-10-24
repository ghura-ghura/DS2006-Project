from sys import exit as sys_exit
from src.types.main import T
from typing import Callable

class Conversion:
    """
    Convert a user input to a specific type.

    Supported type conversions: 
    - input -> int
    - input -> str
    """
    def to(
        self, prompt: str, err_msg: str, cast_type: Callable[[str], T] = int, exit_on_fail: bool = False, additional_checks: Callable[[T], bool] = lambda x: True) -> T:
        try:
            casted_type = cast_type(input(prompt))
            if not additional_checks(casted_type): 
                raise ValueError(err_msg)
            return casted_type
        except ValueError:
            print(err_msg)
            if exit_on_fail:
                sys_exit(1)
            else:
                return self.to(prompt, err_msg, cast_type, exit_on_fail, additional_checks)

    def to_int(self, prompt: str, err_msg: str, exit_on_fail: bool = False, additional_checks: Callable[[int], bool] = lambda x: True) -> int:
        return self.to(prompt, err_msg, int, exit_on_fail, additional_checks)

    def to_str(self, prompt: str, err_msg: str, exit_on_fail: bool = False, additional_checks: Callable[[str], bool] = lambda x: True) -> str:
        return self.to(prompt, err_msg, str, exit_on_fail, additional_checks)

    def to_float(self, prompt: str, err_msg: str, exit_on_fail: bool = False, additional_checks: Callable[[float], bool] = lambda x: True) -> float:
        return self.to(prompt, err_msg, float, exit_on_fail, additional_checks)

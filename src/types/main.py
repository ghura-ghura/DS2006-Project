from pygame import event as pygame_event, Rect
from pandas import DataFrame, Series
from dataclasses import dataclass
from typing import Callable

PyGameEventFunction = Callable[[pygame_event.Event], bool]

ColorFunction = Callable[[int], tuple[int, int, int]]

SetBackRectFunction = Callable[[Rect], None]

SelectorFunction = Callable[[int], None]

@dataclass
class BasicStatistics:
    missing_values: Series
    summary: DataFrame
    data_types: Series

@dataclass
class Dataset:
    train_dataframe_first_x_rows: list[dict[str, str]]
    train_dataframe_basic_statistics: BasicStatistics
    train_dataframe: DataFrame
    loaded_msg: str
    loaded: bool
    path: str

LoadDatasetFunction = Callable[[str, int], Dataset]

TrainModelFunction = Callable[[], None]
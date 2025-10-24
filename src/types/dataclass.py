from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from pandas import DataFrame, Series
from dataclasses import dataclass

@dataclass
class BasicStatistics:
    missing_values: Series
    summary: DataFrame
    data_types: Series

@dataclass
class ModelClassifier:
    model: KNeighborsClassifier | DecisionTreeClassifier
    name: str

@dataclass
class ModelEvaluation:
    model: KNeighborsClassifier | DecisionTreeClassifier
    classification_report: dict | str
    precision: Series
    accuracy: Series
    name: str

@dataclass
class Dataset:
    k_nearest_neighbors_evaluation: ModelEvaluation | None
    train_dataframe_first_x_rows: list[dict[str, str]]
    test_dataframe_first_x_rows: list[dict[str, str]]
    train_dataframe_basic_statistics: BasicStatistics
    decision_tree_evaluation: ModelEvaluation | None
    test_dataframe_basic_statistics: BasicStatistics
    k_nearest_neighbors: ModelClassifier | None
    decision_tree: ModelClassifier | None
    train_dataframe: DataFrame
    test_dataframe: DataFrame
    train_features: DataFrame
    test_features: DataFrame
    train_target: Series
    test_target: Series
    loaded_msg: str
    loaded: bool
    path: str

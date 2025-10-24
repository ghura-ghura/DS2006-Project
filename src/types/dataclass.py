from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from pandas import DataFrame, Series
from dataclasses import dataclass
from datetime import datetime

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
    classification_report: dict
    precisions: Series
    accuracy: float
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

    def to_dict(self, timestamp: float | None = None) -> dict:
        return {
            "timestamp": timestamp if timestamp else datetime.now().timestamp(),
            "loaded_msg": self.loaded_msg,
            "loaded": self.loaded,
            "path": self.path,
            
            "train_dataframe": self.train_dataframe.astype(str).to_dict('records'),
            "test_dataframe": self.test_dataframe.astype(str).to_dict('records'),
            "train_features": self.train_features.astype(str).to_dict('records'),
            "test_features": self.test_features.astype(str).to_dict('records'),
            
            "train_target": self.train_target.tolist(),
            "test_target": self.test_target.tolist(),
            
            "train_dataframe_first_x_rows": self.train_dataframe_first_x_rows,
            "test_dataframe_first_x_rows": self.test_dataframe_first_x_rows,
            
            "train_dataframe_basic_statistics": self.basic_statistics_to_dict(self.train_dataframe_basic_statistics),
            "test_dataframe_basic_statistics": self.basic_statistics_to_dict(self.test_dataframe_basic_statistics),
            
            "k_nearest_neighbors": self.model_classifier_to_dict(self.k_nearest_neighbors) if self.k_nearest_neighbors else None,
            "decision_tree": self.model_classifier_to_dict(self.decision_tree) if self.decision_tree else None,
            
            "k_nearest_neighbors_evaluation": self.evaluation_to_dict(self.k_nearest_neighbors_evaluation),
            "decision_tree_evaluation": self.evaluation_to_dict(self.decision_tree_evaluation)
        }
    
    def evaluation_to_dict(self, evaluation: ModelEvaluation | None) -> dict | None:
        if not evaluation:
            return None

        
        return {
            "classification_report": evaluation.classification_report,
            "precisions": evaluation.precisions.tolist(),
            "model": type(evaluation.model).__name__,
            "accuracy": evaluation.accuracy,
            "name": evaluation.name,
        }

    def basic_statistics_to_dict(self, basic_statistics: BasicStatistics) -> dict:
        return {
            "data_types": basic_statistics.data_types.astype(str).to_dict(),
            "missing_values": basic_statistics.missing_values.to_dict(),
            "summary": basic_statistics.summary.to_dict(),
        }

    def model_classifier_to_dict(self, model_classifier: ModelClassifier) -> dict:
        return {
            "model": type(model_classifier.model).__name__,
            "name": model_classifier.name,
        }
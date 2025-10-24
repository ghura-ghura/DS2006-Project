from src.utils.file import render_available_datasets_and_get_file_name_and_load_dataset
from src.types.dataclass import Dataset, ModelClassifier, ModelEvaluation
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from src.utils.conversion import Conversion
from pandas import DataFrame, Series
from typing import Callable

class EvaluateModel:
    def __init__(self, dataset: Dataset, load_dataset: Callable[[str, int], Dataset]) -> None:
        self.valid_bool_inputs = ["y", "yes", "Y", "Yes", "YES", "n", "no", "N", "No", "NO"]
        self.load_dataset = load_dataset
        self.conversion = Conversion()
        self.dataset = dataset

    def evaluate(self, model_classifier: ModelClassifier) -> ModelEvaluation:
        new_dataset = self.load_additional_dataset_for_evaluation()
        dataset_for_evaluation = new_dataset if new_dataset else self.dataset
        
        predictions = self.predict(model_classifier=model_classifier, features=dataset_for_evaluation.test_features)
        accuracy_score = self.get_accuracy_score(predictions=predictions, dataset=dataset_for_evaluation)
        classification_report = self.get_classification_report(predictions=predictions, dataset=dataset_for_evaluation)

        evaluation = ModelEvaluation(
            classification_report=classification_report,
            model=model_classifier.model,
            name=model_classifier.name,
            accuracy=accuracy_score,
            precisions=predictions,
        )
        return evaluation

    def predict(self, model_classifier: ModelClassifier, features: DataFrame) -> Series:
        predictions = model_classifier.model.predict(features)
        return Series(predictions, index=features.index, name=f"{model_classifier.name} predictions")

    def get_accuracy_score(self, predictions: Series, dataset: Dataset) -> float:
        return accuracy_score(dataset.test_target, predictions)

    def get_classification_report(self, predictions: Series, dataset: Dataset) -> dict:
        return classification_report(dataset.test_target, predictions, output_dict=True, zero_division=0)

    def load_additional_dataset_for_evaluation(self) -> Dataset | None:
        should_use_custom_dataset = self.conversion.to_str(
            prompt=" Do you want to load a seperate dataset for evaluation? (y/n): ",
            additional_checks=lambda input: input in self.valid_bool_inputs,
            err_msg="Please enter a valid response (y/n/yes/no)",
        )

        if should_use_custom_dataset.lower().startswith("n"):
            return None

        print('n')
        dataset = render_available_datasets_and_get_file_name_and_load_dataset(load_dataset=self.load_dataset, conversion=self.conversion, load_rows=10)
        return dataset

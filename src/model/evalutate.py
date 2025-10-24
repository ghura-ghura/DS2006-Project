from src.utils.file import render_available_datasets_and_get_file_name_and_load_dataset
from src.types.dataclass import Dataset, ModelClassifier, ModelEvaluation
from src.utils.conversion import Conversion
from typing import Callable
from pandas import Series

class EvaluateModel:
    def __init__(self, dataset: Dataset, load_dataset: Callable[[str, int], Dataset]) -> None:
        self.valid_bool_inputs = ["y", "yes", "Y", "Yes", "YES", "n", "no", "N", "No", "NO"]
        self.load_dataset = load_dataset
        self.conversion = Conversion()
        self.dataset = dataset

    def evaluate(self, model_classifier: ModelClassifier) -> ModelEvaluation:
        new_dataset = self.load_additional_dataset_for_evaluation()

        if not new_dataset:
            print("No additional dataset loaded. Please load a dataset first.\n")
        
        predictions = self.predict(model_classifier=model_classifier)

        evaluation = ModelEvaluation(
            model=model_classifier.model,
            name=model_classifier.name,
            precision=1.0,
            accuracy=1.0,
        )
        return evaluation

    def predict(self, model_classifier: ModelClassifier) -> Series:
        features = self.dataset.test_features
        predictions = model_classifier.model.predict(features)
        return Series(predictions, index=features.index, name=f"{model_classifier.name} predictions")

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
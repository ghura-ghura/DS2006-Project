from src.types.dataclass import BasicStatistics, Dataset, ModelClassifier, ModelEvaluation
from src.config.main import SUPPORTED_DATASET_EXTENSIONS
from sklearn.neighbors import KNeighborsClassifier
from pandas import Series, read_excel, DataFrame
from sklearn.tree import DecisionTreeClassifier
from src.model.evaluate import EvaluateModel
from src.model.train import TrainModel

class Model:
    def __init__(self) -> None:
        self.evaluate_model_class: EvaluateModel | None = None
        self.train_model_class: TrainModel | None = None
        self.dataset: Dataset | None = None

    def load_dataset(self, file_path: str, load_rows: int = 10) -> Dataset:
        train_dataframe, test_dataframe = self.read_file(file_path)
        
        loaded_successfully_msg = self.dataframes_exist(dataframes=[train_dataframe, test_dataframe])

        train_first_x_rows, test_first_x_rows = self.get_first_x_rows(load_rows, [train_dataframe, test_dataframe])

        train_dataframe_basic_statistics = self.get_basic_statistics(train_dataframe)
        test_dataframe_basic_statistics = self.get_basic_statistics(test_dataframe)

        train_features, train_target = self.split_dataset(train_dataframe)
        test_features, test_target = self.split_dataset(test_dataframe)

        self.dataset = Dataset(
            train_dataframe_basic_statistics=train_dataframe_basic_statistics,
            test_dataframe_basic_statistics=test_dataframe_basic_statistics,
            loaded="successfully" in loaded_successfully_msg.lower(),
            train_dataframe_first_x_rows=train_first_x_rows,
            test_dataframe_first_x_rows=test_first_x_rows,
            k_nearest_neighbors_evaluation=None,
            loaded_msg=loaded_successfully_msg,
            train_dataframe=train_dataframe,
            test_dataframe=test_dataframe,
            train_features=train_features,
            decision_tree_evaluation=None,
            test_features=test_features,
            train_target=train_target,
            k_nearest_neighbors=None,
            test_target=test_target,
            decision_tree=None,
            path=file_path,
        )

        return self.dataset

    def dataframes_exist(self, dataframes: list[DataFrame]) -> str:
        if all(dataframe is not None for dataframe in dataframes):
            return "Dataset loaded successfully"
        
        return f"Failed to load dataset. Please check if the file exists and is in a supported format ({', '.join(SUPPORTED_DATASET_EXTENSIONS)})"
        
    def get_first_x_rows(self, x: int, dataframes: list[DataFrame]) -> list[list[dict[str, str]]]:
        return [dataframe.head(x).to_dict(orient="records") for dataframe in dataframes]

    def get_dataset(self) -> Dataset | None:
        return self.dataset

    def get_basic_statistics(self, dataframe: DataFrame) -> BasicStatistics:
        missing_values: Series = dataframe.isnull().sum()
        data_types: Series = dataframe.dtypes
        summary = dataframe.describe()

        return BasicStatistics(
            missing_values=missing_values,
            data_types=data_types,
            summary=summary,
        )

    def read_file(self, file_path) -> tuple[DataFrame, DataFrame]:
        train_dataframe = read_excel(file_path, sheet_name=1)
        test_dataframe = read_excel(file_path, sheet_name=2)

        train_dataframe.columns = self.clean_columns(train_dataframe)
        test_dataframe.columns = self.clean_columns(test_dataframe)

        relevant_columns = ["STG", "SCG", "STR", "LPR", "PEG", "UNS"]
        train_dataframe = self.get_relevant_columns(dataframe=train_dataframe, columns=relevant_columns)
        test_dataframe = self.get_relevant_columns(dataframe=test_dataframe, columns=relevant_columns)

        return train_dataframe, test_dataframe

    def get_relevant_columns(self, dataframe: DataFrame, columns: list[str]) -> DataFrame:
        return dataframe[columns]

    def clean_columns(self, dataframe: DataFrame) -> DataFrame:
        return dataframe.columns.str.strip().str.upper()

    def split_dataset(self, dataframe: DataFrame) -> tuple[DataFrame, Series]:
        features = dataframe.drop("UNS", axis=1)
        target = dataframe["UNS"]

        return features, target

    def train_model(self, classifier: str, random_state: int | None, n_neighbors: int | None) -> KNeighborsClassifier | DecisionTreeClassifier | None:
        if not self.dataset:
            return None

        if not self.train_model_class:
            self.train_model_class = TrainModel(dataset=self.dataset)
            
        trained_model = self.train_model_class.train(classifier=classifier, random_state=random_state, n_neighbors=n_neighbors)

        setattr(self.dataset, classifier.lower().replace(" ", "_"), ModelClassifier(name=classifier, model=trained_model))

    def evaluate_model(self) -> ModelEvaluation | None:
        if not self.dataset:
            return None

        if not self.evaluate_model_class:
            self.evaluate_model_class = EvaluateModel(dataset=self.dataset, load_dataset=self.load_dataset)

        model_classifier = self.dataset.k_nearest_neighbors if self.dataset.k_nearest_neighbors else self.dataset.decision_tree
        if not model_classifier:
            return None

        evaluation = self.evaluate_model_class.evaluate(model_classifier=model_classifier)
        
        setattr(self.dataset, f"{model_classifier.name.lower().replace(' ', '_')}_evaluation", evaluation)
        return evaluation

    def predict(self, features: DataFrame) -> Series | None:
        if not self.dataset:
            return None

        if not self.evaluate_model_class:
            self.evaluate_model_class = EvaluateModel(dataset=self.dataset, load_dataset=self.load_dataset)

        model_classifier = self.dataset.k_nearest_neighbors if self.dataset.k_nearest_neighbors else self.dataset.decision_tree
        if not model_classifier:
            return None

        return self.evaluate_model_class.predict(features=features, model_classifier=model_classifier)

    def create_new_features_sample(self, features: list[float]) -> DataFrame:
        new_feature_sample = DataFrame([features], columns=["STG", "SCG", "STR", "LPR", "PEG"])
        return new_feature_sample

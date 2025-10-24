from src.utils.file import render_available_datasets_and_get_file_name_and_load_dataset
from src.utils.sys import clear_screen_windows, flush_input_windows
from src.types.dataclass import ModelClassifier
from src.utils.conversion import Conversion
from src.menu.dataset import DatasetMenu
from src.model.main import Model
from typing import Callable

class OptionsMenu:
    def __init__(
        self,
        set_trained_models_options: Callable[[list[str]], None],
        set_show_train_model_options: Callable[[bool], None],
        model: Model,
    ) -> None:
        self.set_show_train_model_options = set_show_train_model_options
        self.set_trained_models_options = set_trained_models_options
        self.conversion = Conversion()
        self.random_state = 42
        self.n_neighbors = 5
        self.model = model

    def on_option_click(self, options: list[str], selected_option: int, is_evaluating: bool) -> None:
        option = options[selected_option]

        match option:
            case "Load dataset":
                dataset = render_available_datasets_and_get_file_name_and_load_dataset(load_dataset=self.model.load_dataset, conversion=self.conversion, load_rows=10)
                self.dataset_menu = DatasetMenu(dataset=dataset)

                clear_screen_windows()
                flush_input_windows()

                self.dataset_menu.render(first_x_rows=10)
            case "Train model":
                if not self.model.get_dataset():
                    print("No dataset loaded. Please load a dataset first.\n")
                    return

                self.set_show_train_model_options(True)
            case "K Nearest Neighbors":
                if not is_evaluating:
                    self.model.train_model(classifier="K Nearest Neighbors", n_neighbors=self.n_neighbors, random_state=None)
                    print("K Nearest Neighbors trained successfully")
                else:
                    self.handle_model_evaluation()

                self.set_show_train_model_options(False)
            case "Decision Tree":
                if not is_evaluating:
                    self.model.train_model(classifier="Decision Tree", random_state=self.random_state, n_neighbors=None)
                    print("Decision Tree trained successfully")
                else:
                    self.handle_model_evaluation()

                self.set_show_train_model_options(False)
            case "Evaluate model":
                dataset = self.model.get_dataset()
                if not dataset:
                    print("No dataset loaded. Please load a dataset and train a model before evaluating.\n")
                    return

                # Filter for trained models
                models: dict[ModelClassifier.name, ModelClassifier.model] = {}
                for trained_model in [dataset.k_nearest_neighbors, dataset.decision_tree]:
                    if not trained_model:
                        continue

                    models[trained_model.name] = trained_model.model

                if not models:
                    print("No trained models found. Please train a model before evaluating.\n")
                    return
                
                self.set_show_train_model_options(False)
                self.set_trained_models_options(list(models.keys()))

    def handle_model_evaluation(self) -> None:
        evaluation = self.model.evaluate_model()
        if not evaluation:
            return
        
        self.dataset_menu = DatasetMenu(dataset=self.model.get_dataset())
        
        clear_screen_windows()
        flush_input_windows()
        
        self.dataset_menu.render_model_evaluation()
        
        input("\nPress Enter to continue...")
        self.set_trained_models_options([])
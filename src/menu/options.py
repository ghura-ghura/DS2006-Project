from src.utils.file import create_folder, render_available_datasets_and_get_file_name_and_load_dataset, write_to_file_json
from src.utils.sys import clear_screen, flush_input, quit
from src.types.dataclass import ModelClassifier
from src.utils.conversion import Conversion
from src.config.main import RESULTS_FOLDER
from src.menu.dataset import DatasetMenu
from src.model.main import Model
from datetime import datetime
from typing import Callable

class OptionsMenu:
    def __init__(
        self,
        set_trained_models_options: Callable[[list[str]], None],
        set_show_train_model_options: Callable[[bool], None],
        set_exiting: Callable[[bool], None],
        model: Model,
    ) -> None:
        self.set_show_train_model_options = set_show_train_model_options
        self.set_trained_models_options = set_trained_models_options
        self.set_exiting = set_exiting
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

                clear_screen()
                flush_input()

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
            case "Predict a target by new features sample":
                dataset = self.model.get_dataset()
                if not dataset:
                    print("No dataset loaded. Please load a dataset and train a model before predicting a target by new features sample.\n")
                    return

                model_classifier = dataset.k_nearest_neighbors if dataset.k_nearest_neighbors else dataset.decision_tree
                if not model_classifier:
                    print("No trained models found. Please train a model before predicting a target by new features sample.\n")
                    return
                
                print("Fill out the following features to create a new feature sample: ")
                err_msg = "Invalid input. Please enter a valid decimal number."

                stg = self.conversion.to_float(prompt="STG (The degree of study time for goal object materails): ", err_msg=err_msg)
                scg = self.conversion.to_float(prompt="SCG (The degree of repetition number of user for goal object materails): ", err_msg=err_msg)
                str = self.conversion.to_float(prompt="STR (The degree of study time of user for related objects with goal object): ", err_msg=err_msg)
                lpr = self.conversion.to_float(prompt="LPR (The exam performance of user for related objects with goal object): ", err_msg=err_msg)
                peg = self.conversion.to_float(prompt="PEG (The exam performance of user for goal objects): ", err_msg=err_msg)

                new_features_sample = self.model.create_new_features_sample(features=[stg, scg, str, lpr, peg])
                prediction = self.model.predict(features=new_features_sample)

                if prediction is None:
                    print("Failed to get prediction. Please try again.")
                else:
                    print(f"The predicted target is {prediction[0]}")

                self.set_show_train_model_options(False)

            case "Save progress to a file":
                dataset = self.model.get_dataset()
                if not dataset:
                    print("No dataset loaded. Please load a dataset before saving the progress to a file.\n")
                    return

                timestamp = datetime.now().timestamp()
                file_name = self.conversion.to_str(
                    prompt="Enter a name for the file: ", 
                    additional_checks=lambda inp: "." not in inp,
                    err_msg="Invalid input. Please enter the file name only (no extensions).",
                )

                create_folder(folder_path=RESULTS_FOLDER)
                write_to_file_json(file_path=f"{RESULTS_FOLDER}/{file_name}_{timestamp}.json", dataset=dataset, timestamp=timestamp)
                print(f"Progress saved successfully to {file_name}")
                quit(set_exiting=self.set_exiting, force_exit=True)

    def handle_model_evaluation(self) -> None:
        evaluation = self.model.evaluate_model()
        if not evaluation:
            return
        
        self.dataset_menu = DatasetMenu(dataset=self.model.get_dataset())
        
        clear_screen()
        flush_input()
        
        self.dataset_menu.render_model_evaluation()
        
        input("\nPress Enter to continue...")
        self.set_trained_models_options([])
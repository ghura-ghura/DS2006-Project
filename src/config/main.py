options = [
    "Load dataset",
    "Train model",
    "Evaluate model",
    "Simulate test dataset",
]

title = "Train a model"

menu_config = {
    "options": options,
    "title": title,
}

train_model_options = [
    "K Nearest Neighbors",
    "Decision Tree",
]

SUPPORTED_DATASET_EXTENSIONS: list[str] = ["xls", "xlsx"]

DATASETS_FOLDER = "datasets"
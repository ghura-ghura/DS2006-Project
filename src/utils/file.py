from src.config.main import DATASETS_FOLDER
from src.utils.conversion import Conversion
from src.types.dataclass import Dataset
from os import listdir, path, makedirs
from src.utils.catch import try_catch
from typing import Callable
from json import dump

def get_file_path_by_name(name: str = "", show_all: bool = False) -> list[str]:
    def _get_files() -> list[str]:
        all_files = listdir(DATASETS_FOLDER)
        
        files = []

        # Filter for files only
        for file in all_files:
            if path.isfile(path.join(DATASETS_FOLDER, file)):
                files.append(file)
        
        if show_all or not name:
            return files
        else:
            # Filter for files that contain the search name
            filtered_files = []
            for file in files:
                if name.lower() in file.lower():
                    filtered_files.append(file)
            return filtered_files
    
    result = try_catch(
        err_msg=f"Dataset folder '{DATASETS_FOLDER}' not found",
        exception=FileNotFoundError,
        include_exception=True,
        callback=_get_files,
    )
    
    return result if result is not None else []

def get_file_name(prompt: str, available_files: list[str], conversion: Conversion) -> str:
        file_name = conversion.to_str(
            additional_checks=lambda file_name: (file_name.isdigit() and available_files[int(file_name) - 1] in available_files) or file_name in available_files,
            err_msg=f"Please enter a valid file name or number",
            prompt=prompt,
        )

        return file_name

def render_available_datasets() -> list[str]:
    files = get_file_path_by_name(show_all=True)

    print("Available datasets:")
    for i,file in enumerate(files):
        print(f"{i + 1}. {file}")
    print("\n")

    return files

def render_available_datasets_and_get_file_name_and_load_dataset(load_dataset: Callable[[str, int], Dataset], conversion: Conversion, load_rows: int) -> Dataset:
    available_datasets = render_available_datasets()

    file_name_or_number = get_file_name(prompt="Select a dataset by name or number: ", available_files=available_datasets, conversion=conversion)
    file_name_or_number = available_datasets[int(file_name_or_number) - 1] if file_name_or_number.isdigit() else file_name_or_number

    dataset = load_dataset(file_path=f"{DATASETS_FOLDER}/{file_name_or_number}", load_rows=load_rows)
    return dataset

def write_to_file_json(file_path: str, dataset: Dataset, timestamp: float | None = None) -> None:
    with open(file_path, "w") as file:
        dump(dataset.to_dict(timestamp=timestamp), file, indent=4)

def create_folder(folder_path: str) -> None:
    if not path.exists(folder_path):
        makedirs(folder_path)
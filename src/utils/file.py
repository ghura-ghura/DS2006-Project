from src.menu.config import DATASETS_FOLDER
from os import listdir, path

def get_file_path_by_name(name: str, show_all: bool = False) -> list[str]:
    """
    Summary:
    
    Get file paths by name from a folder. Optionally show all files in the folder.
    
    Args:
        - name: The name to search for
        - show_all: Whether to show all files
    
    Returns:
        - List of file paths
    """
    try:
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
    except FileNotFoundError:
        return []


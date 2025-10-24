from src.types.dataclass import Dataset

class DatasetMenu:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset
        self.max_width = 0
        self.width = 60

    def render(self, first_x_rows: int = 10) -> None:
        self.render_first_x_rows_for_train_and_test_sets(x=first_x_rows)
        self.render_basic_statistics()

    def render_basic_statistics(self) -> None:
        print("\n" + " " * 20 + "Basic Statistics:")
        print("-" * 120)
        
        train_stats = self.dataset.train_dataframe_basic_statistics.summary
        test_stats = self.dataset.test_dataframe_basic_statistics.summary
        
        train_str = str(train_stats)
        test_str = str(test_stats)
        
        train_lines = train_str.split('\n')
        test_lines = test_str.split('\n')
        
        train_header = "Train Statistics:"
        test_header = "Test Statistics:"
        
        train_padding = " " * (self.width - len(train_header))
        
        print(f"{train_header}{train_padding} | {test_header}")
        print("-" * (self.width + self.width + 3))
        
        max_lines = max(len(train_lines), len(test_lines))
        
        for i in range(max_lines):
            train_line = train_lines[i] if i < len(train_lines) else ""
            test_line = test_lines[i] if i < len(test_lines) else ""
            
            train_line_padding = " " * (self.width - len(train_line))
            print(f"{train_line}{train_line_padding} | {test_line}")
        
        print("-" * (self.width + self.width + 3))
        
    def render_first_x_rows_for_train_and_test_sets(self, x: int = 10) -> None:
        train_data = self.dataset.train_dataframe_first_x_rows[:x]
        test_data = self.dataset.test_dataframe_first_x_rows[:x]
        
        train_header = f"First {x} Rows (Train set):"
        test_header = f"First {x} Rows (Test set):"
        
        max_rows = max(len(train_data), len(test_data))
        max_width = self.width + self.width + 1
        self.max_width = max_width

        print(f"\n{' ' * self.width}{self.dataset.path}")
        print("=" * max_width)

        train_header_padding = " " * (self.width - len(train_header))
        print(f"{train_header}{train_header_padding} | {test_header}")
        print("-" * (max_width + 2))
        
        for i in range(max_rows):
            train_display = self.generate_first_x_rows_display(index=i, data=train_data)
            test_display = self.generate_first_x_rows_display(index=i, data=test_data)
            
            # Print both sides
            if train_display and test_display:
                lines1 = train_display.split('\n')
                lines2 = test_display.split('\n')
                max_lines = max(len(lines1), len(lines2))
                
                for j in range(max_lines):
                    left_line = lines1[j] if j < len(lines1) else ""
                    right_line = lines2[j] if j < len(lines2) else ""
                    left_line_padding = " " * (self.width - len(left_line))
                    print(f"{left_line}{left_line_padding} | {right_line}")

    def generate_first_x_rows_display(self, index: int, data: list[dict[str, str]]) -> str | None:
        if index >= len(data):
            return None

        train_row = data[index]
        train_line1 = self.format_numerical_features(train_row)
        train_line2 = f"UNS: {train_row.get('UNS', 'N/A')}"
        train_display = f"{train_line1}\n{train_line2}"

        return train_display
    
    def format_numerical_features(self, row: dict[str, str]) -> str:
        features = ['STG', 'SCG', 'STR', 'LPR', 'PEG']
        formatted_features = []
        
        for feature in features:
            value = row.get(feature, 'N/A')
            formatted_features.append(f"{feature}: {value}")
        
        return " | ".join(formatted_features) + " |"


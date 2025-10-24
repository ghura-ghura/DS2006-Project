from src.types.dataclass import Dataset

class DatasetMenu:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset
        self.max_width = 0
        self.width = 60

    def render(self, first_x_rows: int = 10) -> None:
        self.render_first_x_rows(x=first_x_rows)
        self.render_basic_statistics()

    def render_model_evaluation(self) -> None:
        evaluations = []
        
        if self.dataset.k_nearest_neighbors_evaluation:
            evaluations.append(self.dataset.k_nearest_neighbors_evaluation)
        if self.dataset.decision_tree_evaluation:
            evaluations.append(self.dataset.decision_tree_evaluation)
        
        if not evaluations:
            print("\nNo model evaluations available.")
            return
        
        for evaluation in evaluations:
            self.render_single_model_evaluation(evaluation)
            print()

    def render_basic_statistics(self) -> None:
        print("\n" + " " * 20 + "Basic Statistics:")
        print("-" * 120)
        
        train_stats = self.dataset.train_dataframe_basic_statistics.summary
        test_stats = self.dataset.test_dataframe_basic_statistics.summary
        
        train_str = str(train_stats)
        test_str = str(test_stats)
        
        self.render_two_column_layout(
            left_header="Train Statistics:",
            right_header="Test Statistics:",
            left_content=train_str,
            right_content=test_str,
        )
        
    def render_first_x_rows(self, x: int = 10) -> None:
        train_data = self.dataset.train_dataframe_first_x_rows[:x]
        test_data = self.dataset.test_dataframe_first_x_rows[:x]
        
        train_header = f"First {x} Rows (Train set):"
        test_header = f"First {x} Rows (Test set):"
        
        max_rows = max(len(train_data), len(test_data))
        max_width = self.width + self.width + 1
        self.max_width = max_width

        print(f"\n{' ' * self.width}{self.dataset.path}")
        print("=" * max_width)

        train_content = self.generate_rows_content(train_data, max_rows)
        test_content = self.generate_rows_content(test_data, max_rows)
        
        self.render_two_column_layout(
            left_content=train_content,
            right_content=test_content,
            left_header=train_header,
            right_header=test_header
        )

    def generate_rows_content(self, data: list[dict[str, str]], max_rows: int) -> str:
        content_lines = []
        for i in range(max_rows):
            display = self.generate_first_x_rows_display(index=i, data=data)
            if display:
                content_lines.append(display)
            else:
                content_lines.append("")
        return "\n".join(content_lines)

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

    def render_single_model_evaluation(self, evaluation) -> None:
        print(f"\n{' ' * 20}Model Evaluation: {evaluation.name}")
        print("-" * 120)
        
        self.render_accuracy(evaluation)
        self.render_predictions(evaluation)
        self.render_classification_report(evaluation)
        
        print("-" * 120)

    def render_accuracy(self, evaluation) -> None:
        accuracy_header = "Accuracy:"
        accuracy_value = f"{evaluation.accuracy:.4f} ({evaluation.accuracy * 100:.2f}%)"
        
        accuracy_width = 50
        accuracy_padding = " " * (accuracy_width - len(accuracy_header))
        print(f"{accuracy_header}{accuracy_padding} | {accuracy_value}")

    def render_predictions(self, evaluation) -> None:
        predictions = evaluation.precisions
        
        unique_predictions = predictions.value_counts()
        total_predictions = len(predictions)
        
        print(f"\nPredictions Summary:")
        print(f"Total predictions: {total_predictions}")
        print(f"Prediction distribution:")
        
        for prediction, count in unique_predictions.items():
            percentage = (count / total_predictions) * 100
            print(f"  {prediction}: {count} ({percentage:.1f}%)")
        
        print(f"\nFirst 10 predictions:")
        for i, pred in enumerate(predictions.head(10)):
            print(f"  {i+1:2d}. {pred}")
        
        if len(predictions) > 10:
            print(f"  ... and {len(predictions) - 10} more")

    def render_classification_report(self, evaluation) -> None:
        report = evaluation.classification_report
        
        print(f"\n{'Classification Report:':<{self.width}} |")
        
        for class_name, metrics in report.items():
            if isinstance(metrics, dict) and class_name not in ['accuracy', 'macro avg', 'weighted avg']:
                self.render_class_metrics(class_name, metrics)
        
        if 'macro avg' in report:
            self.render_class_metrics('Macro Average', report['macro avg'])
        if 'weighted avg' in report:
            self.render_class_metrics('Weighted Average', report['weighted avg'])

    def render_class_metrics(self, class_name: str, metrics: dict) -> None:
        precision = metrics.get('precision', 0)
        recall = metrics.get('recall', 0)
        f1_score = metrics.get('f1-score', 0)
        support = metrics.get('support', 0)
        
        metrics_line = f"{class_name:<15} | Precision: {precision:.3f} | Recall: {recall:.3f} | F1: {f1_score:.3f} | Support: {support}"
        
        if len(metrics_line) > self.width:
            left_part = f"{class_name:<15} | Precision: {precision:.3f} | Recall: {recall:.3f}"
            right_part = f"F1: {f1_score:.3f} | Support: {support}"
            
            left_padding = " " * (self.width - len(left_part))
            print(f"{left_part}{left_padding} | {right_part}")
        else:
            left_padding = " " * (self.width - len(metrics_line))
            print(f"{metrics_line}{left_padding} |")

    def render_two_column_layout(self, left_content: str, right_content: str, left_header: str = "", right_header: str = "") -> None:
        if left_header and right_header:
            left_padding = " " * (self.width - len(left_header))
            print(f"{left_header}{left_padding} | {right_header}")
            print("-" * (self.width + self.width + 3))
        
        left_lines = left_content.split('\n')
        right_lines = right_content.split('\n')
        max_lines = max(len(left_lines), len(right_lines))
        
        for i in range(max_lines):
            left_line = left_lines[i] if i < len(left_lines) else ""
            right_line = right_lines[i] if i < len(right_lines) else ""
            
            left_line_padding = " " * (self.width - len(left_line))
            print(f"{left_line}{left_line_padding} | {right_line}")
        
        print("-" * (self.width + self.width + 3))

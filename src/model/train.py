from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from src.types.dataclass import Dataset

class TrainModel:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def train(self, classifier: str, random_state: int | None, n_neighbors: int | None) -> KNeighborsClassifier | DecisionTreeClassifier | None:
        if classifier == "K Nearest Neighbors" and n_neighbors is not None:
            return self.train_k_nearest_neighbors(n_neighbors)
        elif classifier == "Decision Tree" and random_state is not None:
            return self.train_decision_tree(random_state)
        else:
            print(f"Invalid classifier: {classifier}")
            return None

    def train_k_nearest_neighbors(self, n_neighbors: int) -> KNeighborsClassifier:
        k_nearest_neighbors = KNeighborsClassifier(n_neighbors=n_neighbors)
        k_nearest_neighbors.fit(self.dataset.train_features, self.dataset.train_target)
        return k_nearest_neighbors

    def train_decision_tree(self, random_state: int) -> DecisionTreeClassifier:
        decision_tree = DecisionTreeClassifier(random_state=random_state)
        decision_tree.fit(self.dataset.train_features, self.dataset.train_target)
        return decision_tree

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd 

class Model:
    def __init__(self, dataset_path) -> None:
        # Initialize our model and load the dataset
        self.dataset_path = dataset_path
        self.train_df = None
        self.y_train = None
        self.test_df = None
        self.x_train = None
        self.x_test = None
        self.y_test = None
        

    # Loading the dataset from the path that is given by our user
    def loading_data(self):
         # Load the train data, sheet 1 and clean the columns
         self.train_df = pd.read_excel(self.dataset_path, sheet_name=1)
         self.train_df.columns = self.train_df.columns.str.strip().str.upper()

         # Load the test data, sheet 2 and clean the columns
         self.test_df = pd.read_excel(self.dataset_path, sheet_name=2)
         self.test_df.columns = self.test_df.columns.str.strip().str.upper()

         # Select the relevant columns 
         self.train_df = self.train_df[["STG", "SCG", "STR", "LPR", "PEG", "UNS"]]
         self.test_df = self.test_df[["STG", "SCG", "STR", "LPR", "PEG", "UNS"]]
         
         print("You have loaded the data successfully and only relevant colums are kept, Yay!")

    # Split the data into features and target
    def process_data(self):
        #Normalize labels to aviod duplicate labeles with inconsistent naming and additional underscores etc.
        self.train_df["UNS"] = (
        self.train_df["UNS"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("_", " ")
        )

        self.test_df["UNS"] = (
            self.test_df["UNS"]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace("_", " ")
        )

        # Split train 
        self.x_train = self.train_df.drop("UNS", axis=1)
        self.y_train = self.train_df["UNS"]
       
        # Split test set
        self.x_test = self.test_df.drop("UNS", axis=1)
        self.y_test = self.test_df["UNS"]

        print("You have succesfull split the data, woop woop")

    # Combining the evaluation model to avoid duplicated code in the seperate instances
    def evaluate_model(self, model, model_name):
        predictions = model.predict(self.x_test)
        acc = accuracy_score(self.y_test, predictions)
        print(f"\n {model_name} Evaluation of the results")
        print(f"Accuracy score rounced to two numbers is: {acc:.2f}")
        # Added so we get zero instead of a warning when doing zero division, Got it before... 
        print(classification_report(self.y_test, predictions,zero_division=0))
        print("-" * 40)

    # Train our model 1  KNN since the dataset was already split in train/test we don't do any split. 
    def knn_analysis(self, k=5):
        # Setting K = 5 tried to vary and see outcome
        knn = KNeighborsClassifier(n_neighbors=k)
        # Train our KNN classifier from our training set
        knn.fit(self.x_train, self.y_train)
        self.evaluate_model(knn, f"KNN (k={k})")


        """
        # Obtain our predictions from KNN classifier
        knn_prediction = knn.predict(self.x_test)

        ## Might need to be moved to seperate function
        # Print accuracy of the analysis
        print("Accuracy: ", accuracy_score(self.y_test, knn_prediction))

        #Prints the classification report:
        print(classification_report(self.y_test, knn_prediction))
        """

    # Train our model 2 Tree analysis 
    def decision_tree_analysis(self):
        # Create a decision tree model 
        dt = DecisionTreeClassifier(random_state=77)

        # Trains this DT Classifier with the training set
        dt.fit(self.x_train, self.y_train)
        self.evaluate_model(dt, "Decision Tree")
    
    """
    # Might move to other function.....
        # Obtain the predictions from the d.tree.analysis 
        tree_predict = dt.predict(self.x_test)
        # Print accuracy score & classification report 
        print("Accuracy: ", accuracy_score(self.y_test, tree_predict))
        print(classification_report(self.y_test, tree_predict))
    """



# Testing the loading 
m = Model("dataset/Data_User_Modeling_Dataset_Hamdi Tolga KAHRAMAN.xls")
m.loading_data()
m.process_data()
m.decision_tree_analysis()
m.knn_analysis()


"""
Printing the heads of the datasets -- Might be good to move to main menu
print("\nThe training data contains the first 10 rows\n")
print(m.train_df.head(10))
print(m.train_df.describe())

print("\nThe test data contains the following info\n")
print(m.test_df.head(10))
print(m.test_df.describe())
"""
# Printing the head of the split tests
#print(m.train_df.head())
#print(m.test_df.head())






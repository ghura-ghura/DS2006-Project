import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
import traceback # Just to make it easier when we get errors introduced later..
from datetime import datetime # Just so we can stamp when we do our runs 
import os # So that we can search for our dataset

print("\n🔍 Current working directory:", os.getcwd())
print("📁 __file__:", os.path.abspath(__file__))



class Model:
    def __init__(self, dataset_path=None):
        # Initialize our model and load the dataset path is set to none by default
        self.dataset_path = dataset_path
        self.data_loaded = False # Tracking if data is loaded or not 
        self.model_trained = False # Track if any model has been trained 

        # Tracking KNN models from before
        self.knn_model = None
        self.knn_model_name = None

        # Tracking last DT model
        self.dt_model = None
        self.dt_model_name = None

        # Tracking the last trained model 
        self.last_model = None 
        self.last_model_name = None 

        # Datasets
        self.train_df = None
        self.test_df = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

        # In memory history list 
        self.model_history = []

        # History log for ur runs & printing previous runs if they exist for the file 
        self.history_file = "model_history.txt"
        self.load_history()
    
    # Get the path for the datasets thats relative 
    def get_dataset_path(self, relative_path):
        # Set the path relative to project root 
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(project_root, relative_path)

    # Load previous runs 
    def load_history(self):
        if os.path.exists(self.history_file):
            print("\nprevious model runs: ")
            with open(self.history_file, "r") as f: 
                print(f.read())
        else:
            print("\nNo previous history seems to exist")
    
    # Append new model results to a text file 
    def save_history(self, model_name, acc):
        try: 
            with open(self.history_file, "a") as f: 
                timestamp = datetime.now()
                f.write(f"{timestamp} - {model_name} - Accuracy: {acc:.2f}\n")
            print(f"Results saved to {self.history_file}")

        except Exception as e:
            print("Could not save history: ", e)

    # Loading the dataset from the path that is given by our user
    def loading_data(self, path=None):
        # Check so that the Dataset was entered correctly 
        try: 
            if path:
                self.dataset_path = path
            if not self.dataset_path:
                raise ValueError("No working dataset path has been provided.. Try again..")

            # Load the train data, sheet 1 and clean the columns
            self.train_df = pd.read_excel(self.dataset_path, sheet_name=1)
            self.train_df.columns = self.train_df.columns.str.strip().str.upper()

            # Load the test data, sheet 2 and clean the columns
            self.test_df = pd.read_excel(self.dataset_path, sheet_name=2)
            self.test_df.columns = self.test_df.columns.str.strip().str.upper()

            # Select the relevant columns 
            self.train_df = self.train_df[["STG", "SCG", "STR", "LPR", "PEG", "UNS"]]
            self.test_df = self.test_df[["STG", "SCG", "STR", "LPR", "PEG", "UNS"]]
            
            # Load is seccesful
            self.data_loaded = True
            print("You have loaded the data successfully and only relevant colums are kept, Yay!")

            # Print the head and the basic description for the training/testdata
            print("\nThe training data contains the first 10 rows\n")
            print(self.train_df.head(10))
            print("\n Basic statistic of the training data")
            print(self.train_df.describe())

            print("\nThe test data contains the following info\n")
            print(self.test_df.head(10))
            print("\n Basic statistic of the test data")
            print(self.test_df.describe())
            
        except FileNotFoundError:
            print("File was not found! Check so that the path you entered was correct")
        except ValueError as e:
            print("We got a value error when loading our dataset")
        except Exception as e: 
            print("Unfortunatly we incounted an error when loading the dataset: ", str(e))
            traceback.print_exc()
        
    # Process and split the data into features and target
    def process_data(self):
        # Check if data has been loaded or not
        if not self.data_loaded:
            print("Not possible to process data before the dataset has been loaded")
            return
        try: 

            #Normalize labels to aviod duplicate labeles with inconsistent naming and additional underscores etc. 
            for df in [self.train_df, self.test_df]:
                df.columns = df.columns.str.strip().str.upper()
                df["UNS"] = (
                    df["UNS"]
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

            print("\nYou have succesfull split the data, woop woop")
        except Exception as e: 
            print("Error processing the data: ", str(e))
            traceback.print_exc()

    # Combining the evaluation model to avoid duplicated code in the seperate instances
    def evaluate_model(self, model, model_name):
        try: 
            # Allow the user to specify a different dataset for evaluation 
            use_cust_eval = input("\n Do you want to load a seperate dataset for evaluation? Yes/No: ").strip().lower()
            if use_cust_eval == "yes":
                eval_path = input("Enter the dataset path for evaluation: ").strip()
                # Check so it exists
                if os.path.exists(eval_path):
                    eval_df = pd.read_excel(eval_path)
                    X_eval = eval_df.drop("UNS", axis=1)
                    y_eval = eval_df["UNS"]
                    predictions = model.predict(X_eval)
                else: 
                    print("File not found using default test data instead")
                    predictions = model.predict(self.x_test)
                    y_eval = self.y_test
            else: 
                predictions = model.predict(self.x_test)
                y_eval = self.y_test

            # Create the accuracy score
            acc = accuracy_score(self.y_test, predictions)
            print(f"\n {model_name} Evaluation of the results")
            print(f"Accuracy score rounced to two numbers is: {acc:.2f}")

            # Added so we get zero instead of a warning when doing zero division, Got it before... 
            print(classification_report(self.y_test, predictions,zero_division=0))
            print("-" * 60)

            # Log our results
            self.model_history.append({
                "model": model_name,
                "accuracy": acc,
                "timestamp": datetime.now()
            })

            # Ask user if they want to save the results to a file
            save_res = input("Would you like to save your results to a file? yes or no")
            if save_res == "yes":
                filename = input("Enter the filename that you want to store your results")
                self.save_results(filename)

        except Exception as e:
            print(" Error during model evalutation:", str(e))
            traceback.print_exc()
    
    # To save our results if the user wants that..     
    def save_results(self, filename="results.text"):
        try: 
            with open(filename, "w") as f:
                for record in self.model_history:
                    f.write(f"{record['timestamp']} - {record['model']} - Accuracy: {record['accuracy']:.2f}\n")
            print("\nYou have successfull saved the results to {filename}")

        except Exception as e:
            print("Could unfortunatly not save your results", str(e))


    # Chose wich model to use 
    def chose_model(self, model_type):
        if not self.data_loaded:
            print("\nHold up you need to load and process the dataset before training the model")
            return
        # Making sure the input will match 
        model_type = model_type.lower()

        # Match to the model or specify that it is invalid
        if model_type == "knn":
            self.knn_analysis()
        elif model_type in  ["dt", "decision_tree"]:
            self.decision_tree_analysis()
        else:
            print("This model type is unknown, {model_type}. Chose either knn or decision_tree")


    # Train our model 1  KNN since the dataset was already split in train/test we don't do any split. 
    def knn_analysis(self, k=5):
        try: 
            # Setting K = 5 tried to vary and see outcome
            knn = KNeighborsClassifier(n_neighbors=k)
            # Train our KNN classifier from our training set
            knn.fit(self.x_train, self.y_train)

            # Track this model so it is the last KNN and last model 
            self.knn_model = knn
            self.knn_model_name = f"KNN (k={k})"
            self.last_model = knn
            self.last_model_name =self.knn_model_name
            self.model_trained = True 

            self.evaluate_model(knn, self.knn_model_name)
        
        except Exception as e:
            print("We got an error during our KNN analysis", str(e))
            traceback.print_exc()


    # Train our model 2 Tree analysis 
    def decision_tree_analysis(self, random_state=77):
        try: 
            # Create a decision tree model 
            dt = DecisionTreeClassifier(random_state=random_state)

            # Trains this DT Classifier with the training set
            dt.fit(self.x_train, self.y_train)

            # Track this model so it is the last DT and last model overall
            self.dt_model = dt
            self.dt_model_name = "Decision Tree"
            self.last_model = dt 
            self.last_model_name = self.dt_model_name
            self.model_trained = True

            # Evaluate the model
            self.evaluate_model(dt, self.dt_model_name)
        
        except Exception as e: 
            print("\nHoly moly we got an error when running the DT-model")
            traceback.print_exc()
    
    def predict_by_example(self):
        if not self.model_trained:
            print("\nHey ho, you must first train a model before making predictions.. ")
            return
        try:
            print("\n Enter values for the new example that you want to try predict class for: ")
            stg = float(input("STG(The degree of study time for goal object materails): \n"))
            scg = float(input("SCG(The degree of repetition number of user for goal object materails): \n"))
            strr = float(input("STRR(The degree of study time of user for related objects with goal object): \n"))
            lpr = float(input("LPRLPR(The exam performance of user for related objects with goal object): \n"))
            peg = float(input("PEGPEG (The exam performance of user for goal objects): \n"))

            # Format input so that it is suitable for analysis 
            new_data_ex = pd.DataFrame([[stg,scg,strr,lpr,peg]], columns=["STG", "SCG", "STR", "LPR", "PEG"])

            # Predict by drawing from the last model we used
            prediction = self.last_model.predict(new_data_ex)
            print(f"The predicted class is {prediction[0]}")

        except Exception as e:
            print("Error during the ex prediction: ", str(e))
            traceback.print_exc()

    # Make it so we can seach for our datasets
    def list_availible_data(self, dataset_dir="dataset"):
        # Serching for the files in the datasets folder
        try: 
            # Resolve relative to the project root so we don't get error when trying to chose the file 
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dataset_path = os.path.join(base_dir, dataset_dir)
            print(f"Looking for datasets in: {dataset_path}")

            if not os.path.exists(dataset_path):
                print("The dataset folder {dataset_path} wasn't found.. ")
                return None 
            
            #find dataset files
            files = [f for f in os.listdir(dataset_path) if f.endswith((".xls", ".xlsx", ".csv"))]
            print(f"Found files {files}")
            if not files:
                print("Echo no datasets found in the {dataset_dir}")
                return None
            
            # List all avalible datasets
            print("\nAvalible datasets")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}") 
            
            # Let the user pick from the numbered list 
            choice = input("\nEnter the number of the dataset: ").strip()
            # Check so that user choses in the range of files and default to 0 if they don't make a choice 
            selected = files[0] if not choice else files[int(choice) - 1]
            full_path = os.path.join(dataset_path, selected)
            print(f"✅ You selected: {full_path}")
            return full_path
           
            """
            if not choice:
                selected = files[0]
            elif choice.isdigit() and 1 <= int(choice) <= len(files):
                return files[int(choice)-1]
            else:
                print("\nThats not a valid option m8")
                return None 
            """
            # Return our full path
            full_path = os.path.join(dataset_path, selected)
            print(f"\n You have selected: {full_path}")
            return full_path
        
        except Exception as e:
            print("We got an error whilst listing the datasets", str(e))
            traceback.print_exc()
            return None 


    # Resetting the model to initial values 
    def reset(self):
        dataset_path = self.dataset_path
        self.__init__(dataset_path)
        print("Model state has been reset")
    
    # Just so we can run everything
    def run_everything(self):
        print("\n --- Test console ---")
        while True:
            print("\n Your playing opions")
            print("1. Load dataset")
            print("2. Train one of the two models, knn / decision_tree")
            print("3. Predict by new example")
            print("4. Exit")

            choice = input("Select option: ").strip()
            if choice == "1": 
                path = self.list_availible_data()
                if not path:
                    print("\n No dataset found")
                    continue
                self.loading_data(path)
                if self.data_loaded:
                    self.process_data()
            elif choice == "2":
                model_type = input("Which model do you want to train? knn / decision_tree: ")
                self.chose_model(model_type)
            elif choice == "3":
                self.predict_by_example()
            elif choice == "4": 
                print("\nExiting program, cee ya!")
                break
            else: 
                print("Thats not a valid option mate")

    
# Testing the loading 
m = Model()
dataset_path = m.get_dataset_path("dataset/Data_User_Modeling_Dataset_Hamdi Tolga KAHRAMAN.xls")
m.loading_data(dataset_path)
m.run_everything()
"""
When we want to run this from our main program
if __name__ == "__main__":
    m = Model("dataset/Data_User_Modeling_Dataset_Hamdi Tolga KAHRAMAN.xls")
    m.run_everything()
"""





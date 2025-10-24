# Data Science Machine Learning Project

A comprehensive machine learning application for dataset analysis, model training, and evaluation with an interactive terminal-based menu system.

## 🎯 Project Overview

This project provides a complete machine learning pipeline for educational data analysis, featuring:

-   **Interactive Terminal Menu**: Cross-platform navigation with arrow keys and keyboard shortcuts
-   **Dataset Management**: Load and process Excel datasets with automatic train/test splitting
-   **Model Training**: Support for K-Nearest Neighbors and Decision Tree classifiers
-   **Model Evaluation**: Comprehensive evaluation with accuracy metrics and classification reports
-   **Data Visualization**: Display dataset statistics, sample data, and model performance
-   **Progress Saving**: Export complete project state to JSON files
-   **Cross-Platform Support**: Works on Windows, Linux, and macOS

## 🏗️ Architecture

### Project Structure

```
project/
├── main.py                 # Application entry point
├── datasets/               # Input datasets (Excel files)
├── results/               # Exported JSON files
├── src/
│   ├── config/            # Configuration and constants
│   ├── menu/              # User interface components
│   ├── model/             # Machine learning logic
│   ├── types/             # Data structures and type definitions
│   └── utils/             # Utility functions and helpers
└── README.md
```

### Core Components

#### 🧠 **Model Layer** (`src/model/`)

-   **`main.py`**: Core Model class handling dataset loading, training, and evaluation
-   **`train.py`**: Model training implementations (KNN, Decision Tree)
-   **`evaluate.py`**: Model evaluation with metrics and cross-validation

#### 🎨 **User Interface** (`src/menu/`)

-   **`main.py`**: Main menu controller with cross-platform key handling
-   **`options.py`**: Menu option handlers and user interactions
-   **`dataset.py`**: Dataset visualization and statistics display
-   **`key.py`**: Cross-platform keyboard input handling

#### 📊 **Data Management** (`src/types/`)

-   **`dataclass.py`**: Type-safe data structures for datasets, models, and evaluations
-   **`main.py`**: Generic type definitions

#### 🔧 **Utilities** (`src/utils/`)

-   **`file.py`**: File I/O operations and dataset loading
-   **`conversion.py`**: Type conversion and input validation
-   **`sys.py`**: System operations (screen clearing, input flushing)
-   **`catch.py`**: Error handling utilities

## 🚀 Features

### 📈 **Dataset Management**

-   **Multi-format Support**: Excel files (.xls, .xlsx)
-   **Automatic Processing**: Train/test split with feature extraction
-   **Data Validation**: Missing value detection and data type analysis
-   **Sample Preview**: Display first N rows of training and test data

### 🤖 **Machine Learning Models**

-   **K-Nearest Neighbors**: Configurable k parameter
-   **Decision Tree**: Random state control for reproducibility
-   **Cross-Platform Training**: Consistent results across operating systems

### 📊 **Model Evaluation**

-   **Accuracy Metrics**: Precision, recall, F1-score, and support
-   **Classification Reports**: Detailed per-class performance analysis
-   **Prediction Analysis**: Sample predictions and distribution statistics
-   **Cross-Dataset Evaluation**: Option to evaluate on different datasets

### 💾 **Data Persistence**

-   **JSON Export**: Complete project state serialization
-   **Timestamp Tracking**: Automatic timestamp generation for exports
-   **Progress Saving**: Save and resume work sessions

### 🎮 **User Experience**

-   **Interactive Navigation**: Arrow keys (↑↓) or W/S keys for menu navigation
-   **Keyboard Shortcuts**: Enter to select, Esc to quit
-   **Cross-Platform**: Works on Windows, Linux, and macOS
-   **Real-time Feedback**: Immediate visual feedback for all operations

## 🛠️ Installation & Setup

### Prerequisites

-   Python 3.8+
-   Required packages (see requirements below)

### Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd project
    ```

2. **Install dependencies**:

    ```bash
    pip install pandas scikit-learn openpyxl
    ```

3. **Prepare datasets**:
    - Place Excel files in the `datasets/` folder
    - Ensure files have two sheets: training data (sheet 1) and test data (sheet 2)
    - Required columns: `STG`, `SCG`, `STR`, `LPR`, `PEG`, `UNS`

### Running the Application

```bash
python main.py
```

## 📋 Usage Guide

### 🎯 **Main Menu Options**

1. **Load Dataset**

    - Browse available datasets
    - Select by name or number
    - Automatic data validation and processing

2. **Train Model**

    - Choose between K-Nearest Neighbors or Decision Tree
    - Configure model parameters
    - Automatic training and validation

3. **Evaluate Model**

    - Select trained model for evaluation
    - Option to use different dataset for evaluation
    - Comprehensive performance metrics

4. **Predict Target**

    - Input new feature values
    - Get predictions from trained models
    - Real-time prediction feedback

5. **Save Progress**
    - Export complete project state to JSON
    - Automatic timestamp generation
    - Resume work from saved state

### ⌨️ **Navigation Controls**

| **Action**        | **Windows**  | **Linux/Mac** | **Description**         |
| ----------------- | ------------ | ------------- | ----------------------- |
| **Navigate Up**   | ↑ Arrow or W | ↑ Arrow or W  | Move to previous option |
| **Navigate Down** | ↓ Arrow or S | ↓ Arrow or S  | Move to next option     |
| **Select**        | Enter        | Enter         | Choose current option   |
| **Quit**          | Esc          | Esc           | Exit application        |

### 📊 **Dataset Format Requirements**

Your Excel files should have:

-   **Sheet 1**: Training data
-   **Sheet 2**: Test data
-   **Required Columns**: `STG`, `SCG`, `STR`, `LPR`, `PEG`, `UNS`
-   **Target Column**: `UNS` (for classification)

## 🔧 Technical Details

### 🏗️ **Architecture Patterns**

-   **MVC Pattern**: Separation of model, view, and controller logic
-   **Factory Pattern**: Model creation and configuration
-   **Strategy Pattern**: Different evaluation strategies
-   **Observer Pattern**: Menu state management

### 🎯 **Key Features**

-   **Type Safety**: Comprehensive type hints and dataclasses
-   **Error Handling**: Graceful error recovery and user feedback
-   **Cross-Platform**: Automatic platform detection and adaptation
-   **Modular Design**: Clean separation of concerns

### 📈 **Performance Optimizations**

-   **Lazy Loading**: Models and datasets loaded on demand
-   **Memory Management**: Efficient data structure usage
-   **Input Buffering**: Optimized keyboard input handling

## 🧪 **Supported Models**

### K-Nearest Neighbors

-   **Algorithm**: KNN with configurable k parameter
-   **Use Case**: Non-parametric classification
-   **Parameters**: Number of neighbors (default: 5)

### Decision Tree

-   **Algorithm**: CART decision tree
-   **Use Case**: Interpretable classification
-   **Parameters**: Random state for reproducibility

## 📊 **Evaluation Metrics**

-   **Accuracy**: Overall classification accuracy
-   **Precision**: Per-class precision scores
-   **Recall**: Per-class recall scores
-   **F1-Score**: Harmonic mean of precision and recall
-   **Support**: Number of samples per class

## 🔄 **Data Flow**

1. **Dataset Loading** → Data validation → Train/test split
2. **Model Training** → Parameter configuration → Model fitting
3. **Model Evaluation** → Prediction generation → Metrics calculation
4. **Results Display** → Statistics visualization → Performance analysis
5. **Progress Saving** → State serialization → JSON export

## 🐛 **Troubleshooting**

### Common Issues

-   **Dataset Loading**: Ensure Excel files have correct sheet structure
-   **Model Training**: Check that dataset is loaded before training
-   **Cross-Platform**: Keyboard input may vary between systems

### Error Handling

-   **Graceful Degradation**: Application continues on non-critical errors
-   **User Feedback**: Clear error messages and recovery suggestions
-   **Input Validation**: Robust input checking and type conversion

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is part of DS2006 coursework and is intended for educational purposes.

## 🎓 **Educational Value**

This project demonstrates:

-   **Machine Learning Pipeline**: End-to-end ML workflow
-   **Software Engineering**: Clean code principles and design patterns
-   **User Interface Design**: Terminal-based interactive applications
-   **Cross-Platform Development**: Platform-agnostic code
-   **Data Science**: Real-world data analysis and model evaluation

---

**Built with ❤️ for Data Science Education**

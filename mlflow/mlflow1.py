import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pandas as pd

# Set MLflow tracking URI (using local directory)
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("iris_classification")

# Load and prepare data
iris = load_iris()
X = iris.data
y = iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10],
    'min_samples_split': [2, 5]
}

# Function to train and evaluate model
def train_and_evaluate(params):
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_params(params)
        
        # Create and train model
        model = RandomForestClassifier(**params, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return accuracy, run.info.run_id

# Perform grid search
best_accuracy = 0
best_run_id = None

for n_estimators in param_grid['n_estimators']:
    for max_depth in param_grid['max_depth']:
        for min_samples_split in param_grid['min_samples_split']:
            params = {
                'n_estimators': n_estimators,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split
            }
            
            accuracy, run_id = train_and_evaluate(params)
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_run_id = run_id

print(f"Best run ID: {best_run_id}")
print(f"Best accuracy: {best_accuracy}")

# Serve the model using MLflow
#model_uri = f"runs:/{best_run_id}/model"
#mlflow.models.serve(model_uri, port=1234)

"""
# In a separate Python script or notebook, you can make predictions using the served model:

import requests
import numpy as np

# Sample data for prediction
sample_data = {
    "dataframe_split": {
        "columns": ["sepal length", "sepal width", "petal length", "petal width"],
        "data": [[5.1, 3.5, 1.4, 0.2]]
    }
}

# Make prediction request
response = requests.post("http://127.0.0.1:1234/invocations", 
                        json=sample_data,
                        headers={"Content-Type": "application/json"})

print("Prediction:", response.json())
"""

"""
# Alternatively, you can use curl:
curl -X POST -H "Content-Type:application/json" \
    --data '{"dataframe_split": {"columns":["sepal length", "sepal width", "petal length", "petal width"], "data":[[5.1, 3.5, 1.4, 0.2]]}}' \
    http://127.0.0.1:1234/invocations
"""
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def get_model():
    # Load iris dataset as an example
    X, y = load_iris(return_X_y=True)
    
    # Train a simple random forest classifier
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X, y)
    
    return clf

# Initialize the model
model = get_model() 
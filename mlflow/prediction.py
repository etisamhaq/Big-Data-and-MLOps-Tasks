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
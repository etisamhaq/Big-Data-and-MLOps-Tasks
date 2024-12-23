from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import socket
from model import model

app = FastAPI()

class PredictionInput(BaseModel):
    features: list[float]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "container_id": socket.gethostname()
    }

@app.post("/predict")
def predict(input_data: PredictionInput):
    # Convert input to numpy array
    features = np.array(input_data.features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(features)
    
    return {
        "prediction": int(prediction[0]),
        "container_id": socket.gethostname()
    } 
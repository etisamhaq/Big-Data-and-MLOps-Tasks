from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pickle
import numpy as np
from datetime import datetime
import time
import os
from train_model import preprocess_text

app = Flask(__name__)
CORS(app)

# Load the pre-trained model and vectorizer
with open('model/sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    
    try:
        # Get input data
        data = request.json
        text = data['text']
        
        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Vectorize text
        text_vectorized = vectorizer.transform([processed_text])
        
        # Generate prediction
        prediction = model.predict(text_vectorized)[0]
        prediction_proba = model.predict_proba(text_vectorized)[0]
        
        # Map prediction to sentiment
        sentiment = "Positive" if prediction == 1 else "Negative"
        confidence = prediction_proba[1] if prediction == 1 else prediction_proba[0]
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Log to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO Log (Current_Date_Time, Input_Params, Output, Response_Time)
        VALUES (%s, %s, %s, %s)
        """
        
        output_data = {
            'sentiment': sentiment,
            'confidence': float(confidence)
        }
        
        cursor.execute(
            insert_query,
            (
                datetime.now(),
                text,
                str(output_data),
                response_time
            )
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'confidence': float(confidence),
            'response_time': response_time
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
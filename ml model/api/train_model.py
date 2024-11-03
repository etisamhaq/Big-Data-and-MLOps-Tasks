import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
import nltk
from nltk.corpus import stopwords
import re

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

# Create sample dataset
data = {
    'text': [
        "This product is amazing! I love it!",
        "Terrible experience, would not recommend",
        "Pretty good but could be better",
        "Absolutely horrible service",
        "Great customer support and quality",
        # Add more examples here
    ],
    'sentiment': [1, 0, 1, 0, 1]  # 1 for positive, 0 for negative
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Preprocess the text
df['processed_text'] = df['text'].apply(preprocess_text)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    df['processed_text'], 
    df['sentiment'], 
    test_size=0.2, 
    random_state=42
)

# Create and fit the vectorizer
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train the model
model = LogisticRegression(random_state=42)
model.fit(X_train_vectorized, y_train)

# Create model directory if it doesn't exist
import os
os.makedirs('model', exist_ok=True)

# Save the model and vectorizer
with open('model/sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model training completed and saved!")

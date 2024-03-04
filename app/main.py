import os
import pickle
import uvicorn
from fastapi import FastAPI
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app import schemas
from app import preprocessing as pp

app = FastAPI()

# Load the pre-trained TensorFlow model
model = tf.keras.models.load_model("app/models/sms_spam_prediction.keras")

# Load tokenizer for text processing
with open("app/models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

@app.post("/predict", response_model=schemas.SentimentResponse)
async def predict_sentiment(request: schemas.SentimentRequest):
    text = pp.text_cleaning(request.text)

    # Tokenize and pad the input text
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, maxlen=20)

    # Make predictions
    predictions = model.predict(padded_sequences)
    probability = predictions[0][0]

    # Determine sentiment based on the threshold (adjust as needed)
    sentiment = "Positive" if probability >= 0.5 else "Negative"

    return {"sentiment": sentiment, "probability": float(probability)}
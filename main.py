from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import random
from datetime import date
import pandas as pd
import os

# Handle the custom transformer required by the pickled model
class DenseTransformer:
    def fit(self, X, y=None): return self
    def transform(self, X): return X.toarray()

app = FastAPI()

# Load model - ensure this file is uploaded to your repo
# Or use an absolute path if using a persistent disk
model_path = "sklearn_sentiment_model.pkl"
loaded_model = joblib.load(model_path)

class SentimentRequest(BaseModel):
    foodId: str
    Food: str
    comments: str

NAMES = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Ethan Hunt"]

@app.get("/")
def home():
    return {"status": "Server is running"}

@app.post("/analyze_food")
def analyze_food(request: SentimentRequest):
    try:
        prediction = loaded_model.predict([request.comments])[0]
        confidence = float(loaded_model.predict_proba([request.comments]).max())
        star_map = {"POSITIVE": 5, "NEUTRAL": 3, "NEGATIVE": 1}
        stars = star_map.get(prediction, 3)

        return {
            "customerName": random.choice(NAMES),
            "date": str(date.today()),
            "sentiment_results": {
                "label": prediction, 
                "confidence": round(confidence, 4), 
                "star_rating": stars
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
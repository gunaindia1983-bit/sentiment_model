# This updated cell fixes the AttributeError by defining DenseTransformer BEFORE loading the model
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import random
from datetime import date
import pandas as pd
import os

# 1. Define the custom transformer FIRST so joblib can find it
# class DenseTransformer:
#     def fit(self, X, y=None): return self
#     def transform(self, X): return X.toarray()

app = FastAPI()

# 2. Load model - referencing the same filename expected in the repo
model_path = "sklearn_sentiment_model.pkl"
if os.path.exists(model_path):
    loaded_model = joblib.load(model_path)
else:
    loaded_model = None

class SentimentRequest(BaseModel):
    foodId: str
    Food: str
    comments: str

NAMES = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Ethan Hunt"]

@app.get("/")
def home():
    return {"status": "Server is running", "model_loaded": loaded_model is not None}

@app.post("/analyze_food")
def analyze_food(request: SentimentRequest):
    if not loaded_model:
        raise HTTPException(status_code=500, detail="Model file not found on server.")
    
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

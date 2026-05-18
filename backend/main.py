from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import os

# ---- Load your advanced ensemble model ----
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ensemble_model.pkl')

app = FastAPI(title="Football Prediction Backend", description="API for match outcome predictions.")

# ---- Request/response schema ----
class MatchData(BaseModel):
    features: list  # Input feature vector (list of numbers)

class PredictionResponse(BaseModel):
    probabilities: list
    prediction: int

# ---- Load model at startup ----
@app.on_event("startup")
def load_model():
    global model
    global model_classes
    if os.path.exists(MODEL_PATH):
        obj = pickle.load(open(MODEL_PATH, "rb"))
        model = obj["ensemble"]
        scaler = obj["scaler"]
        model_classes = obj["classes"]
        app.state.scaler = scaler
    else:
        model = None
        model_classes = None

@app.get("/")
def root():
    return {"status": "ok", "message": "Football Prediction API is running!"}

@app.post("/predict", response_model=PredictionResponse)
def predict(match: MatchData):
    if model is None:
        raise HTTPException(status_code=500, detail="Prediction model unavailable.")
    try:
        # Model expects a 2D array
        arr = np.array(match.features).reshape(1, -1)
        arr_scaled = app.state.scaler.transform(arr)
        probabilities = model.predict_proba(arr_scaled)[0]
        pred_class = int(model.predict(arr_scaled)[0])
        return PredictionResponse(probabilities=probabilities.tolist(), prediction=pred_class)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

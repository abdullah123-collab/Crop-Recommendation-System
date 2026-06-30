from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class PredictRequest(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    temperature: float
    humidity: float
    rainfall: float


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
MODEL_DIR = ROOT_DIR / "models" / "crop_rec"
MODEL_PATH = MODEL_DIR / "crop_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"
FRONTEND_DIR = ROOT_DIR / "frontend"

FEATURE_ORDER = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def load_model_artifacts():
    required_files = [MODEL_PATH, SCALER_PATH, ENCODER_PATH]
    if not all(path.exists() for path in required_files):
        raise FileNotFoundError("One or more trained model files are missing from the models/crop_rec folder.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoder = joblib.load(ENCODER_PATH)
    return model, scaler, encoder


model, scaler, encoder = load_model_artifacts()

app = FastAPI(
    title="AI Crop Advisor",
    description="FastAPI backend serving the crop recommendation frontend.",
    version="1.0.0",
)


@app.post("/api/predict")
async def predict_crop(data: PredictRequest):
    try:
        values = [
            data.nitrogen,
            data.phosphorus,
            data.potassium,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall,
        ]

        features = np.array([values], dtype=float)
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]
        predicted_crop = str(encoder.inverse_transform([prediction])[0])

        probabilities = model.predict_proba(scaled_features)[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [str(encoder.inverse_transform([idx])[0]) for idx in top_indices]
        confidence_score = round(float(probabilities[top_indices[0]]) * 100, 2)

        return JSONResponse(
            {
                "recommended_crop": predicted_crop,
                "confidence_score": confidence_score,
                "message": f"Based on your soil and weather data, {predicted_crop} is the best fit.",
                "top_3_predictions": top_predictions,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

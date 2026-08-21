import joblib
import numpy as np
from pathlib import Path
from backend.schemas.crop import PredictRequest

class CropService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoder = None
        self.load_models()

    def load_models(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        model_dir = base_dir / "models" / "crop_rec"
        model_path = model_dir / "crop_model.pkl"
        scaler_path = model_dir / "scaler.pkl"
        encoder_path = model_dir / "label_encoder.pkl"

        # Validate that required model files exist
        for path in [model_path, scaler_path, encoder_path]:
            if not path.exists():
                raise FileNotFoundError(f"Required model artifact is missing: {path}")

        # Load model artifacts
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.encoder = joblib.load(encoder_path)

    def predict(self, payload: PredictRequest) -> dict:
        # Build feature vector in the EXACT SAME ORDER as the current implementation
        values = [
            payload.nitrogen,
            payload.phosphorus,
            payload.potassium,
            payload.temperature,
            payload.humidity,
            payload.ph,
            payload.rainfall
        ]
        
        features = np.array([values], dtype=float)
        
        # Apply the existing scaler
        scaled_features = self.scaler.transform(features)
        
        # Run the existing Random Forest model
        prediction = self.model.predict(scaled_features)[0]
        
        # Decode the prediction using the existing LabelEncoder
        predicted_crop = str(self.encoder.inverse_transform([prediction])[0])
        
        # Calculate prediction probabilities and return top 3 predictions
        probabilities = self.model.predict_proba(scaled_features)[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [str(self.encoder.inverse_transform([idx])[0]) for idx in top_indices]
        
        # Calculate confidence using the highest probability
        confidence_score = round(float(probabilities[top_indices[0]]) * 100, 2)
        
        return {
            "recommended_crop": predicted_crop,
            "confidence_score": confidence_score,
            "message": f"Based on your soil and weather data, {predicted_crop} is the best fit.",
            "top_3_predictions": top_predictions
        }

# Reusable crop_service instance
crop_service = CropService()

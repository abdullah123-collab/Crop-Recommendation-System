from pathlib import Path

import gradio as gr
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
    description="FastAPI backend serving crop recommendations through a Gradio interface.",
    version="1.0.0",
)


def build_prediction_response(payload: dict | PredictRequest) -> dict:
    if isinstance(payload, PredictRequest):
        payload_dict = payload.model_dump()
    elif isinstance(payload, dict):
        payload_dict = payload
    else:
        raise TypeError("Payload must be a PredictRequest instance or a dictionary.")

    values = [
        payload_dict["nitrogen"],
        payload_dict["phosphorus"],
        payload_dict["potassium"],
        payload_dict["temperature"],
        payload_dict["humidity"],
        payload_dict["ph"],
        payload_dict["rainfall"],
    ]

    features = np.array([values], dtype=float)
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)[0]
    predicted_crop = str(encoder.inverse_transform([prediction])[0])

    probabilities = model.predict_proba(scaled_features)[0]
    top_indices = np.argsort(probabilities)[::-1][:3]
    top_predictions = [str(encoder.inverse_transform([idx])[0]) for idx in top_indices]
    confidence_score = round(float(probabilities[top_indices[0]]) * 100, 2)

    return {
        "recommended_crop": predicted_crop,
        "confidence_score": confidence_score,
        "message": f"Based on your soil and weather data, {predicted_crop} is the best fit.",
        "top_3_predictions": top_predictions,
    }


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "message": "AI Crop Advisor backend is running."}


@app.post("/api/predict")
async def predict_crop(data: PredictRequest):
    try:
        return JSONResponse(build_prediction_response(data))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


def gradio_predict(nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall):
    try:
        result = build_prediction_response(
            {
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "ph": ph,
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
            }
        )
        return (
            result["recommended_crop"],
            f"{result['confidence_score']}%",
            ", ".join(result["top_3_predictions"]),
            result["message"],
        )
    except Exception as exc:
        return "Prediction unavailable", "N/A", "N/A", f"Prediction failed: {exc}"


with gr.Blocks(
    theme=gr.themes.Soft(),
    css="""
    .gradio-container { max-width: 1100px !important; }
    .panel { padding: 1.25rem; border-radius: 1rem; background: #f6fff7; }
    """,
) as demo:
    gr.Markdown(
        "# 🌾 AI Crop Advisor\n"
        "Smart crop recommendations powered by soil and weather conditions."
    )

    with gr.Row():
        with gr.Column(scale=1):
            nitrogen = gr.Number(label="Nitrogen (N)", value=48.0, minimum=0, maximum=150, step=0.5)
            phosphorus = gr.Number(label="Phosphorus (P)", value=34.0, minimum=0, maximum=150, step=0.5)
            potassium = gr.Number(label="Potassium (K)", value=42.0, minimum=0, maximum=150, step=0.5)
            ph = gr.Number(label="pH Level", value=6.7, minimum=0, maximum=14, step=0.1)

        with gr.Column(scale=1):
            temperature = gr.Number(label="Temperature (°C)", value=28.0, minimum=-10, maximum=50, step=0.5)
            humidity = gr.Number(label="Humidity (%)", value=72.0, minimum=0, maximum=100, step=1)
            rainfall = gr.Number(label="Rainfall (mm)", value=85.0, minimum=0, maximum=400, step=1)

    predict_button = gr.Button("Predict Best Crop")

    with gr.Row():
        with gr.Column(scale=1):
            crop_output = gr.Textbox(label="Recommended Crop", interactive=False)
        with gr.Column(scale=1):
            confidence_output = gr.Textbox(label="Confidence Score", interactive=False)

    top_output = gr.Textbox(label="Top Predictions", interactive=False)
    message_output = gr.Textbox(label="Message", interactive=False)

    predict_button.click(
        gradio_predict,
        inputs=[nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall],
        outputs=[crop_output, confidence_output, top_output, message_output],
    )

    gr.Markdown("This interface reuses the existing FastAPI prediction pipeline and trained model artifacts.")


demo.queue()
app = gr.mount_gradio_app(app, demo, path="/")

# AI Crop Advisor

AI Crop Advisor is a FastAPI application that serves a Gradio-based crop recommendation interface. The project keeps the existing machine learning pipeline and trained model artifacts while exposing them through a polished UI and a production-ready API.

## 📁 Project Structure

```text
crop_recommendation_project/
├── backend/
│   ├── main.py
│   └── utils/
│       ├── fertilizer.py
│       └── weather.py
├── data/
│   └── tabular/
│       └── Crop_recommendation.csv
├── models/
│   └── crop_rec/
│       ├── crop_model.pkl
│       ├── scaler.pkl
│       └── label_encoder.pkl
├── scripts/
│   ├── train_model.py
│   ├── generate_assets.py
│   └── notebooks/
│       └── model.ipynb
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

1. Activate your virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 7860
   ```
4. Open the Gradio UI at:
   ```bash
   http://127.0.0.1:7860/
   ```
5. The prediction API remains available at:
   ```bash
   http://127.0.0.1:7860/api/predict
   ```

## 🧠 Train or Update the Model

If you want to retrain the model using the dataset, run:

```bash
python scripts/train_model.py
```

This script regenerates the crop model artifacts in the models/crop_rec folder.

## 🐳 Docker

Build the Docker image:
```bash
docker build -t ai-crop-advisor .
```

Run locally:
```bash
docker run -p 7860:7860 ai-crop-advisor
```

## ☁️ Hugging Face Spaces

This repository is ready for a Docker-based Hugging Face Space. Use the existing Dockerfile and requirements, then deploy with the command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 7860
```

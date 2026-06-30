# AI Crop Advisor

AI Crop Advisor is a polished FastAPI application that recommends the best crop based on soil and weather features. The project now uses a cleaner separation between the backend, frontend, data, models, and supporting scripts.

## 📁 Project Structure

```text
crop_recommendation_project/
├── backend/
│   ├── main.py
│   └── utils/
│       ├── fertilizer.py
│       └── weather.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── assets/
├── models/
│   └── crop_rec/
│       ├── crop_model.pkl
│       ├── scaler.pkl
│       └── label_encoder.pkl
├── data/
│   └── tabular/
│       └── Crop_recommendation.csv
├── scripts/
│   ├── train_model.py
│   ├── generate_assets.py
│   └── notebooks/
│       └── model.ipynb
├── legacy_streamlit/
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
3. Start the FastAPI app:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 7860
   ```
4. Open the UI at:
   ```bash
   http://127.0.0.1:7860
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

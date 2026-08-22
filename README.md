# 🌱 AI Agriculture Advisor

> An AI-powered agriculture advisor for crop recommendations and future plant disease detection.

AI Agriculture Advisor combines a trained crop recommendation model with a **FastAPI backend** and a browser-based frontend.

The project preserves the existing machine learning pipeline and trained model artifacts while exposing the prediction system through an API and user interface.

---

## ✨ Features

* 🌱 **Crop Recommendation** — Predict a suitable crop from soil and environmental parameters
* 🤖 **Machine Learning Model** — Uses a trained ML model for crop prediction
* ⚡ **FastAPI Backend** — Provides a prediction API for programmatic access
* 🩺 **Disease Detection Foundation** — Provides image upload and model-unavailable handling for the future disease model
* 📊 **Data Processing** — Uses preprocessing components including a scaler and label encoder
* 🔄 **Model Retraining** — Includes a training script for updating the model
* 🐳 **Docker Support** — Includes a Docker configuration for containerized execution
* ☁️ **Hugging Face Ready** — Structured for deployment as a Docker-based Hugging Face Space

---

## 🧠 How It Works

The application follows a simple machine learning prediction pipeline:

```text
User Input
    │
    ▼
Input Processing
    │
    ▼
Feature Scaling
    │
    ▼
Trained ML Model
    │
    ▼
Label Decoding
    │
    ▼
Recommended Crop
```

The trained model receives the required soil/environmental inputs, applies the saved preprocessing components, and returns the predicted crop.

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │      User Input     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Browser Frontend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Preprocessing     │
                    │ Scaler + Encoder    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Trained ML Model   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Recommended Crop    │
                    └─────────────────────┘
```

---

## 📁 Project Structure

```text
crop_recommendation_project/
│
├── backend/
│   ├── main.py
│   └── utils/
│       ├── fertilizer.py
│       └── weather.py
│
├── data/
│   └── tabular/
│       └── Crop_recommendation.csv
│
├── models/
│   └── crop_rec/
│       ├── crop_model.pkl
│       ├── scaler.pkl
│       └── label_encoder.pkl
│
├── scripts/
│   ├── train_model.py
│   ├── generate_assets.py
│   └── notebooks/
│       └── model.ipynb
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🤖 Machine Learning

The project uses a trained machine learning model together with saved preprocessing artifacts.

### Model Artifacts

| File                | Purpose                       |
| ------------------- | ----------------------------- |
| `crop_model.pkl`    | Trained crop prediction model |
| `scaler.pkl`        | Feature scaling               |
| `label_encoder.pkl` | Encoding/decoding crop labels |

The training workflow is maintained in:

```text
scripts/train_model.py
```

The associated notebook is available at:

```text
scripts/notebooks/model.ipynb
```

---

## 📊 Dataset

The project uses a tabular crop recommendation dataset:

```text
data/tabular/Crop_recommendation.csv
```

The dataset is used as the source for training the crop recommendation model.

---

## ⚡ FastAPI Backend

The backend is implemented using **FastAPI**.

Main backend entry point:

```text
backend/main.py
```

The prediction API is available locally at:

```text
POST /api/crop/predict
POST /api/disease/predict
GET  /health
```

The API allows the prediction functionality to be accessed independently from the user interface.

---

## 🖥️ Browser Interface

The frontend is served directly by FastAPI. It includes crop recommendation and a disease detection upload workflow. Disease analysis reports that the model is unavailable until a trained model is added; it never returns fabricated disease predictions.

---

## 🚀 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/abdullah123-collab/Crop-Recommendation-System.git
cd Crop-Recommendation-System
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Application

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 7860
```

### 5. Open the Application

Browser interface:

```text
http://127.0.0.1:7860/
```

Prediction API:

```text
http://127.0.0.1:7860/api/crop/predict
```

Disease prediction API:

```text
http://127.0.0.1:7860/api/disease/predict
```

---

## 🔄 Retrain the Model

The project includes a training script that can be used to retrain the model using the available dataset.

```bash
python scripts/train_model.py
```

The generated model artifacts are stored in:

```text
models/crop_rec/
```

---

## 🐳 Docker

The project includes a `Dockerfile` for containerized execution.

### Build the Image

```bash
docker build -t ai-crop-advisor .
```

### Run the Container

```bash
docker run -p 7860:7860 ai-crop-advisor
```

After starting the container, open:

```text
http://127.0.0.1:7860/
```

---

## ☁️ Hugging Face Spaces

The repository is structured for a **Docker-based Hugging Face Space**.

The Docker configuration binds to `0.0.0.0` and uses the `PORT` environment variable, defaulting to `7860`.

Application command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}
```

---

## 🛠️ Tech Stack

### Machine Learning

* Python
* Scikit-learn
* Pandas
* NumPy
* Jupyter Notebook

### Backend

* FastAPI
* Uvicorn

### Interface

* HTML, CSS, and JavaScript frontend

### Deployment

* Docker
* Hugging Face Spaces

### Development

* Git
* GitHub

---

## 📌 Project Status

**Active Development**

The current project includes:

* Machine learning crop recommendation
* Saved model artifacts
* FastAPI prediction backend
* Disease detection upload architecture without fake predictions
* Model retraining workflow
* Docker support
* Hugging Face Space configuration

Further improvements and refinements are planned as development continues.

---

## 🔮 Future Improvements

Potential improvements include:

* Improving model performance
* Adding additional agricultural data
* Expanding prediction capabilities
* Improving the user interface
* Adding more detailed prediction insights
* Enhancing deployment and production configuration

---

## 👨‍💻 Author

**Muhammad Abdullah**

BSCS Student | Data Science | Machine Learning | Python

GitHub: [@abdullah123-collab](https://github.com/abdullah123-collab)

---

## 📄 License

This project is available under the license included in the repository.

---

## ⭐ About the Project

AI Agriculture Advisor was developed as a practical machine learning project to explore the complete workflow from **data and model training to API-based prediction and deployment**.

The project demonstrates how a trained machine learning model can be transformed into an accessible application using **FastAPI, a browser frontend, Docker, and Hugging Face Spaces**.

# 🌱 AI Crop Advisor

> An AI-powered crop recommendation application that uses machine learning to recommend suitable crops based on soil and environmental conditions.

AI Crop Advisor combines a trained machine learning model with a **FastAPI backend** and a **Gradio-based interface** to provide an accessible crop recommendation workflow.

The project preserves the existing machine learning pipeline and trained model artifacts while exposing the prediction system through an API and user interface.

---

## ✨ Features

* 🌱 **Crop Recommendation** — Predict a suitable crop from soil and environmental parameters
* 🤖 **Machine Learning Model** — Uses a trained ML model for crop prediction
* ⚡ **FastAPI Backend** — Provides a prediction API for programmatic access
* 🖥️ **Gradio Interface** — Provides a user-friendly interface for making predictions
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
                    │    Gradio UI        │
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
http://127.0.0.1:7860/api/predict
```

The API allows the prediction functionality to be accessed independently from the user interface.

---

## 🖥️ Gradio Interface

The application provides a Gradio-based interface for interacting with the crop recommendation system.

After starting the application, the interface is available at:

```text
http://127.0.0.1:7860/
```

Users can provide the required input values and receive a crop recommendation through the interface.

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

Gradio interface:

```text
http://127.0.0.1:7860/
```

Prediction API:

```text
http://127.0.0.1:7860/api/predict
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

The existing Docker configuration can be used for deployment, with the application running on port `7860`.

Application command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 7860
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

* Gradio

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
* Gradio interface
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

AI Crop Advisor was developed as a practical machine learning project to explore the complete workflow from **data and model training to API-based prediction and deployment**.

The project demonstrates how a trained machine learning model can be transformed into an accessible application using **FastAPI, Gradio, Docker, and Hugging Face Spaces**.

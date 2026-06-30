import json
from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "Crop_recommendation.csv"
MODEL_PATH = BASE_DIR / "model" / "crop_model.pkl"

st.set_page_config(page_title="Dataset Analytics | AI Crop Advisor", page_icon="📈", layout="wide")

st.markdown("""
# 📊 Dataset Analytics
Explore the dataset, distribution, and the trained model behind AI Crop Advisor.
""")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


df = load_data()
model = load_model()

col1, col2, col3 = st.columns(3)
col1.metric("Records", len(df))
col2.metric("Crop classes", df["label"].nunique())
col3.metric("Missing values", int(df.isna().sum().sum()))

st.markdown("---")

with st.expander("Dataset preview", expanded=True):
    st.dataframe(df.head(10))

with st.container():
    st.subheader("Crop Distribution")
    crop_counts = df["label"].value_counts().rename_axis("crop").reset_index(name="count")
    fig_crop = px.bar(
        crop_counts,
        x="crop",
        y="count",
        color="count",
        color_continuous_scale="Greens",
        labels={"crop": "Crop", "count": "Records"},
    )
    fig_crop.update_layout(showlegend=False, xaxis_title="Crop", yaxis_title="Count")
    st.plotly_chart(fig_crop, use_container_width=True)

with st.container():
    st.subheader("Missing Values Analysis")
    missing = df.isna().sum()
    missing_df = missing[missing > 0].reset_index()
    missing_df.columns = ["feature", "missing_count"]
    if missing_df.empty:
        st.success("No missing values found in the dataset.")
    else:
        st.table(missing_df)

with st.container():
    st.subheader("Feature Correlation Heatmap")
    corr = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Greens",
        labels={"x": "Feature", "y": "Feature", "color": "Correlation"},
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with st.container():
    st.subheader("Feature Importance")
    feature_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=True)
    fig_importance = px.bar(
        importance_df,
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale="Greens",
        labels={"importance": "Importance", "feature": "Feature"},
    )
    st.plotly_chart(fig_importance, use_container_width=True)

with st.expander("Training metrics and report", expanded=False):
    metrics_path = BASE_DIR / "model" / "model_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        st.metric("Model accuracy", f"{metrics['accuracy'] * 100:.2f}%")
        report_df = pd.DataFrame(metrics["report"]).transpose()
        st.dataframe(report_df.style.format({"precision": "{:.2f}", "recall": "{:.2f}", "f1-score": "{:.2f}"}))
    else:
        st.warning("Model metrics file is not available. Run model/train_model.py to generate it.")

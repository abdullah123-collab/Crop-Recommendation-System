import io
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_PATH = BASE_DIR / "prediction_history.csv"

st.set_page_config(page_title="Prediction History | AI Crop Advisor", page_icon="📜", layout="wide")

st.markdown("""
# 📜 Prediction History
All saved predictions are stored here for review and export.
""")

if HISTORY_PATH.exists():
    history = pd.read_csv(HISTORY_PATH)
    st.metric("Total saved predictions", len(history))
    st.dataframe(history.sort_values(by="date", ascending=False).reset_index(drop=True))

    csv_bytes = history.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download history as CSV",
        data=csv_bytes,
        file_name="prediction_history.csv",
        mime="text/csv",
    )
else:
    st.warning("No prediction history is available yet. Run a crop prediction from the home page to create the first record.")

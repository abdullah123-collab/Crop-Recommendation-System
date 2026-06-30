import streamlit as st
import pickle
import numpy as np

# 1. Page Configuration (Hamesha sab se pehle likhein)
st.set_page_config(
    page_title="Crop Recommender AI",
    page_icon="🌾",
    layout="centered"
)

# 2. Custom CSS for Frontend Styling
st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #f8fbf8;
    }
    /* Main Heading Styling */
    h1 {
        color: #2e7d32;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    /* Predict Button Styling */
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
        border: 1px solid #2e7d32;
    }
    /* Result Box Styling */
    .result-box {
        padding: 20px;
        background-color: #e8f5e9;
        border-left: 6px solid #2e7d32;
        border-radius: 8px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Model Loading with Caching for Fast Performance
@st.cache_resource
def load_models():
    model = pickle.load(open('crop_model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    encoder = pickle.load(open('label_encoder.pkl', 'rb'))
    return model, scaler, encoder

model, scaler, encoder = load_models()

# 4. Sidebar Design
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913584.png", width=120)
    st.header("🌾 About Project")
    st.write("Yeh ek **Machine Learning** based Crop Recommendation System hai.")
    st.write("Aapki zameen ki mitti (Nitrogen, Phosphorus, Potassium) aur mausam (Temperature, Humidity, Rainfall) ka data use kar ke AI best fasal tajweez karta hai.")
    st.markdown("---")
    st.write("Developed with ❤️ using Streamlit")

# 5. Main UI Header
st.markdown("<h1>🌾 AI Crop Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #555;'>Apni zameen aur mausam ki tafseelaat darj karein, aur humara ML model behtareen fasal suggest karega.</p>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("📊 Soil & Weather Parameters")

# 6. Inputs Layout (3 Columns for better UI)
col1, col2, col3 = st.columns(3)

with col1:
    N = st.number_input("🧪 Nitrogen (N)", min_value=0.0, max_value=150.0, value=50.0, step=1.0, help="Mitti mein Nitrogen ki miqdar")
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, format="%.2f")
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=400.0, value=100.0, format="%.2f")

with col2:
    P = st.number_input("🧪 Phosphorus (P)", min_value=0.0, max_value=150.0, value=50.0, step=1.0, help="Mitti mein Phosphorus ki miqdar")
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=70.0, format="%.2f")

with col3:
    K = st.number_input("🧪 Potassium (K)", min_value=0.0, max_value=150.0, value=50.0, step=1.0, help="Mitti mein Potassium ki miqdar")
    ph = st.number_input("⚗️ pH Level", min_value=0.0, max_value=14.0, value=6.5, format="%.2f", help="Zameen ka pH level (Ideal: 6-7)")

st.markdown("<br>", unsafe_allow_html=True)

# 7. Prediction Logic with Loading Spinner
if st.button("🔮 Recommend Best Crop"):
    # Spinner animation while processing
    with st.spinner("AI is analyzing your soil and weather data..."):
        
        # Prepare input array
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        # Transform and Predict
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)
        crop_name = encoder.inverse_transform(prediction)[0]
        
        # Display nicely formatted result
        st.markdown(f"""
            <div class="result-box">
                <h2 style='color: #2e7d32; margin:0;'>🎉 Recommendation: {crop_name.upper()}</h2>
                <p style='margin:0; font-size: 16px; color: #333;'>In halaat ke mutabiq aapki zameen ke liye <strong>{crop_name.capitalize()}</strong> ki kashatkari sab se behtareen rahay gi.</p>
            </div>
        """, unsafe_allow_html=True)
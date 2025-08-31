# smartagro_app.py

import streamlit as st
from PIL import Image
import joblib
import numpy as np
import random
from datetime import datetime, timedelta
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")

# --- LANGUAGE OPTIONS ---
LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi"
}

# --- TEXTS (always keep English as fallback) ---
TEXT = {
    "en": {
        "title": "SmartAgro AI – Your Farm's Smart Assistant",
        "welcome": "Welcome! Use our AI tools for smarter farming decisions.",
        "tab_crop": "🌾 Crop Recommendation",
        "tab_health_diagnosis": "🌿 Field Health Diagnosis",
        "tab_profit": "💰 Profit Forecast",
        "tab_water": "💧 AI Water Advisor",
        "tab_harvest": "📈 Harvest Advisor",
        "tab_wellness": "💚 Wellness Tips",
        "tab_sms": "📱 SMS/IVR Demo",
        "header_crop": "Find the Perfect Crop & Get a Cultivation Guide",
        "uploader_soil": "Upload Soil Image",
        "button_analyze_soil": "Analyze Soil",
        "header_health": "AI Field Doctor",
        "uploader_health": "Upload plant image",
        "button_diagnose": "Diagnose Now",
        "header_profit": "Profit Forecast",
        "button_forecast": "Calculate Forecast for {crop}",
        "header_water": "Water Advisor",
        "button_water_advice": "Get Water Advice",
        "header_harvest": "Harvest Advisor",
        "button_harvest_advice": "Get Harvest Advice",
        "header_wellness": "Wellness Tips",
        "header_sms_demo": "SMS/IVR Demo",
        "button_send_sms": "Simulate SMS"
    },
    "kn": {},  # Kannada translations can be filled later
    "hi": {}   # Hindi translations can be filled later
}

# --- LOAD MODEL ---
@st.cache_resource
def load_crop_model():
    try:
        if os.path.exists("crop_model.pkl"):
            model = joblib.load("crop_model.pkl")
            return model
        else:
            st.warning("⚠️ crop_model.pkl not found in repo root. Using fallback dummy model.")
            class DummyModel:
                def predict(self, X): return ["rice"]
            return DummyModel()
    except Exception as e:
        st.error(f"Fatal Error loading crop_model.pkl → {e}")
        class DummyModel:
            def predict(self, X): return ["rice"]
        return DummyModel()

crop_model = load_crop_model()

# --- SIMPLE AI FUNCTIONS ---
def analyze_soil_image(image_file):
    with Image.open(image_file) as img:
        avg_color = np.array(img.convert("RGB")).mean(axis=(0, 1))
        brightness = sum(avg_color) / 3
        if brightness < 80:
            return {"soil_type": "Clay Loam", "organic_matter": "High"}
        elif brightness < 140:
            return {"soil_type": "Loamy Soil", "organic_matter": "Moderate"}
        else:
            return {"soil_type": "Sandy Soil", "organic_matter": "Low"}

def predict_crop(data):
    return crop_model.predict([data])[0]

def get_watering_advice():
    return random.choice([
        "No watering needed today (rain expected).",
        "Water for 20 minutes in the morning.",
        "Deep watering for 45 minutes recommended."
    ])

def get_harvest_advice():
    return random.choice([
        "Harvest in the next 3 days to avoid rain.",
        "Wait 1 more week for better market prices.",
        "Harvest anytime in the next 10 days."
    ])

# --- APP LAYOUT ---
st.sidebar.title("🌍 Language")
lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
lang_code = LANGUAGES[lang_display]

# ✅ Always fallback to English safely
T = TEXT.get(lang_code) or TEXT["en"]

st.title(T["title"])
st.write(T["welcome"])

tabs = st.tabs([
    T["tab_crop"], T["tab_health_diagnosis"], T["tab_profit"],
    T["tab_water"], T["tab_harvest"], T["tab_wellness"], T["tab_sms"]
])

# --- CROP RECOMMENDATION TAB ---
with tabs[0]:
    st.header(T["header_crop"])
    soil_img = st.file_uploader(T["uploader_soil"], type=["jpg","jpeg","png"])
    if soil_img and st.button(T["button_analyze_soil"], key="analyze_soil"):
        res = analyze_soil_image(soil_img)
        st.success(f"Soil type: **{res['soil_type']}**, Organic Matter: **{res['organic_matter']}**")

# --- FIELD HEALTH TAB ---
with tabs[1]:
    st.header(T["header_health"])
    health_img = st.file_uploader(T["uploader_health"], type=["jpg","jpeg","png"])
    if health_img and st.button(T["button_diagnose"], key="diagnose"):
        st.info("Threat detected: Fall Armyworm 🐛 → Use pheromone traps.")

# --- PROFIT FORECAST TAB ---
with tabs[2]:
    st.header(T["header_profit"])
    if st.button(T["button_forecast"].format(crop="Rice"), key="forecast"):
        st.success("Estimated Revenue: ₹45,000 per acre.")

# --- WATER ADVISOR TAB ---
with tabs[3]:
    st.header(T["header_water"])
    if st.button(T["button_water_advice"], key="water"):
        st.success(get_watering_advice())

# --- HARVEST ADVISOR TAB ---
with tabs[4]:
    st.header(T["header_harvest"])
    if st.button(T["button_harvest_advice"], key="harvest"):
        st.success(get_harvest_advice())

# --- WELLNESS TIPS TAB ---
with tabs[5]:
    st.header(T["header_wellness"])
    st.markdown("- Add compost regularly\n- Rotate crops\n- Use neem oil spray")

# --- SMS DEMO TAB ---
with tabs[6]:
    st.header(T["header_sms_demo"])
    phone = st.text_input("📞 Enter phone number", "9876543210", max_chars=10)
    if st.button(T["button_send_sms"], key="sms"):
        st.success(f"SMS sent to {phone}: Best crop for your soil is Rice 🌾")

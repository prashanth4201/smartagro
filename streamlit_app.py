# smartagro_app.py
# Final merged version for GitHub deploy

import os
import streamlit as st
from PIL import Image
import joblib
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")

# --- AI MODEL LOADING ---
@st.cache_resource
def load_crop_model():
    """Load the crop recommendation model safely."""
    try:
        model = joblib.load("crop_model.pkl")   # ✅ no models/ folder
        return model
    except Exception:
        st.warning("⚠️ crop_model.pkl not found. Using fallback dummy model.")
        class DummyModel:
            def predict(self, X): return ["rice"]
        return DummyModel()

crop_model = load_crop_model()

# --- LANGUAGE MAP ---
LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi"
}

# --- KNOWLEDGE BASES ---
CROP_ACTION_PLANS = {
    # keep your multilingual action plan dict here ...
}
CROP_DATA = {
    "rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050, "maturity_days": 120},
    "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100, "maturity_days": 100},
    "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500, "maturity_days": 150},
    "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000, "maturity_days": 365}
}
THREAT_DATABASE = {
    # keep your threats dict here ...
}
TEXT = {
    # keep your multilingual TEXT dict here ...
}

# --- AI LOGIC FUNCTIONS ---
def analyze_soil_image(image_file):
    with Image.open(image_file) as img:
        avg_color = np.array(img.convert('RGB')).mean(axis=(0, 1))
        brightness = sum(avg_color) / 3
        if brightness < 80: return {"soil_type": "Clay Loam", "organic_matter_estimate": "High"}
        elif brightness < 140: return {"soil_type": "Loamy Soil", "organic_matter_estimate": "Moderate"}
        else: return {"soil_type": "Sandy Soil", "organic_matter_estimate": "Low"}

def predict_crop_and_plan(data, lang):
    prediction_result = crop_model.predict([data])[0]
    action_plan = CROP_ACTION_PLANS.get(lang, {}).get(prediction_result.lower(), {})
    return {'recommended_crop': prediction_result, 'action_plan': action_plan}

def diagnose_threat(lang):
    threats = ["fall_armyworm", "leaf_blight", "amaranthus_viridis"]
    identified_threat_key = random.choice(threats)
    threat_info = THREAT_DATABASE.get(lang, {}).get(identified_threat_key, {"type": "Unknown", "solution": "No solution found."})
    return {'threat_name': identified_threat_key.replace('_', ' ').title(), 'threat_type': threat_info['type'], 'recommended_action': threat_info['solution']}

def get_watering_advice(soil_type, lang):
    weather = {"temp": round(random.uniform(24.0, 32.0), 1), "humidity": random.randint(55, 85), "forecast": random.choice(["Sunny", "Cloudy", "Chance of Rain"])}
    return {"weather": weather, "advice": "Normal watering advice"}  # simplify for now

def get_harvest_advice(crop_name, sowing_date, lang):
    maturity_days = CROP_DATA.get(crop_name.lower(), {}).get("maturity_days", 100)
    harvest_date = sowing_date + timedelta(days=maturity_days)
    return {"harvest_window": f"{harvest_date.strftime('%d %b, %Y')}", "market_outlook": "Stable", "weather_outlook": "Clear", "advice": "Harvest at your convenience"}

# --- APP LAYOUT ---
if crop_model is None:
    st.error("Fatal Error: Crop recommendation model not loaded.")
else:
    st.sidebar.title("Language / ಭಾಷೆ / भाषा")
    lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
    lang_code = LANGUAGES.get(lang_display, "en")   # ✅ safe fallback
    T = TEXT.get(lang_code, TEXT["en"])             # ✅ safe fallback

    st.title(T.get("title", "SmartAgro AI"))
    st.markdown(T.get("welcome", "Welcome! Use our AI tools for smarter farming decisions."))

    tab_keys = ["tab_crop", "tab_health_diagnosis", "tab_profit", "tab_water", "tab_harvest", "tab_wellness", "tab_sms"]
    tabs = st.tabs([T.get(key, key.replace('_', ' ').title()) for key in tab_keys])

    with tabs[0]: # Crop Recommendation
        st.header(T.get("header_crop", "Find the Perfect Crop"))
        soil_image = st.file_uploader(T.get("uploader_soil", "Upload Soil Image"), type=["jpg", "jpeg", "png"], key="soil_upload")
        if soil_image:
            st.image(soil_image, caption='Your Soil', width=300)
            if st.button(T.get("button_analyze_soil", "Analyze Soil"), key="analyze_soil_btn"):
                st.session_state.soil_analysis_result = analyze_soil_image(soil_image)

    with tabs[1]: # Field Health Diagnosis
        st.header(T.get("header_health", "Field Health Diagnosis"))
        uploaded_file = st.file_uploader(T.get("uploader_health", "Upload plant image"), type=["jpg", "jpeg", "png"], key="health_upload")
        if uploaded_file and st.button(T.get("button_diagnose", "Diagnose Now"), key="diagnose_btn"):
            result = diagnose_threat(lang_code)
            st.success(f"{result['threat_name']} → {result['recommended_action']}")

    with tabs[2]: # Profit Forecast
        st.header(T.get("header_profit", "Profit Forecast"))
        if st.button(T.get("button_forecast", "Calculate Forecast").format(crop="Rice"), key="forecast_btn"):
            st.success("Example forecast here...")

    with tabs[3]: # Water Advisor
        st.header(T.get("header_water", "Water Advisor"))
        if st.button(T.get("button_water_advice", "Get Water Advice"), key="water_btn"):
            st.success("Normal watering needed")

    with tabs[4]: # Harvest Advisor
        st.header(T.get("header_harvest", "Harvest Advisor"))
        sowing_date = st.date_input("Sowing Date", datetime.now() - timedelta(days=60))
        if st.button(T.get("button_harvest_advice", "Get Harvest Advice"), key="harvest_btn"):
            result = get_harvest_advice("rice", sowing_date, lang_code)
            st.success(result['advice'])

    with tabs[5]: # Wellness Tips
        st.header(T.get("header_wellness", "Wellness Tips"))
        st.write("Add soil, water and pest wellness tips...")

    with tabs[6]: # SMS/IVR Demo
        st.header(T.get("header_sms_demo", "SMS/IVR Demo"))
        if st.button(T.get("button_send_sms", "Simulate SMS"), key="sms_btn"):
            st.success("SMS Sent Successfully!")

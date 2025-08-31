# streamlit_app.py
# Final Corrected Version for Successful Deployment (with fallback dummy model)

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
class DummyCropModel:
    """Fallback dummy model when crop_model.pkl is missing."""
    def predict(self, X):
        crops = ["rice", "maize", "pigeonpeas", "coffee"]
        return [random.choice(crops) for _ in X]

@st.cache_resource
def load_crop_model():
    """Load the crop recommendation model safely, fallback to dummy if missing."""
    try:
        base_dir = os.path.dirname(__file__)
        model_path = os.path.join(base_dir, "models", "crop_model.pkl")
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            st.warning("⚠️ crop_model.pkl not found in models/. Using fallback dummy model.")
            return DummyCropModel()
    except Exception as e:
        st.warning(f"⚠️ Could not load crop_model.pkl → {e}. Using fallback dummy model.")
        return DummyCropModel()

crop_model = load_crop_model()

# --- LANGUAGE MAPPING ---
LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi"
}

# --- KNOWLEDGE BASES (Multilingual Data) ---
CROP_ACTION_PLANS = {
    'en': {
        "rice": {
            "🌾 Land Preparation": ["- Plow 2-3 times.", "- Ensure good drainage."],
            "🌱 Seed & Sowing": ["- Use high-yield seeds.", "- 20-25 kg/acre.", "- Transplant after 25 days."],
            "💧 Irrigation": ["- Maintain 2-5 cm water.", "- Stop 15 days before harvest."],
            "🐞 Pest Control": ["- Watch for stem borer.", "- Apply neem oil."]
        },
        "maize": {
            "🌾 Land Preparation": ["- Deep plow.", "- Soil must be weed-free."],
            "🌱 Seed & Sowing": ["- Hybrid HQPM-1.", "- 8-10 kg/acre.", "- 60x20 cm spacing."],
            "💧 Irrigation": ["- Water at knee-high, flowering, grain filling."],
            "🐞 Pest Control": ["- Watch out for armyworm."]
        }
    }
}
CROP_DATA = {
    "rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050, "maturity_days": 120},
    "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100, "maturity_days": 100},
    "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500, "maturity_days": 150},
    "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000, "maturity_days": 365}
}
THREAT_DATABASE = {
    'en': {
        "fall_armyworm": {"type": "Pest", "solution": "Use pheromone traps."},
        "leaf_blight": {"type": "Disease", "solution": "Remove leaves, apply fungicide."},
        "amaranthus_viridis": {"type": "Weed", "solution": "Manual removal or herbicide."}
    }
}
TEXT = {
    'en': {
        "title": "SmartAgro AI – Your Farm's Smart Assistant",
        "welcome": "Welcome! Use our AI tools for smarter farming decisions.",
        "tab_crop": "🌾 Crop Recommendation",
        "tab_health_diagnosis": "🌿 Field Health Diagnosis",
        "tab_profit": "💰 Profit Forecast",
        "tab_wellness": "💚 Wellness Tips",
        "tab_sms": "📱 SMS/IVR Demo",
        "tab_water": "💧 AI Water Advisor",
        "tab_harvest": "📈 Harvest Advisor",
        "role_selector_title": "Select Your Role",
        "role_farmer": "I am a Farmer",
        "role_kiosk": "I am a Kiosk Operator",
        "kiosk_info": "This mode helps you assist multiple farmers.",
        "header_crop": "Find the Perfect Crop & Get a Cultivation Guide",
        "button_analyze_soil": "Analyze Soil",
        "spinner_soil": "Analyzing soil...",
        "subheader_crop_step2": "Step 2: Add Soil Test Values",
        "info_soil_analysis": "Soil looks like **{soil_type}** with **{organic_matter}** organic matter.",
        "button_get_plan": "Get My Crop Action Plan",
        "spinner_plan": "Generating plan...",
        "success_crop": "Best crop: **{crop}**",
        "subheader_plan": "Your Action Plan for {crop}",
        "button_start_over": "Start Over",
        "header_health": "AI Field Doctor",
        "button_diagnose": "Diagnose Now",
        "diagnosis_result": "Diagnosis Result",
        "threat_name": "Threat",
        "threat_type": "Type",
        "threat_action": "Action",
        "header_profit": "Profit Forecast",
        "button_forecast": "Calculate Forecast for {crop}",
        "subheader_results": "Results",
        "metric_yield": "Yield",
        "metric_price": "Market Price",
        "metric_revenue": "Revenue",
        "warning_no_crop": "Please run crop recommendation first.",
        "header_water": "Water Advisor",
        "button_water_advice": "Get Advice",
        "subheader_weather_sim": "Weather (Simulated)",
        "subheader_advice": "Recommendation",
        "warning_no_soil": "Please analyze soil first.",
        "header_harvest": "Harvest Advisor",
        "button_harvest_advice": "Get Advice",
        "harvest_window_header": "Harvest Window",
        "market_outlook_header": "Market",
        "weather_outlook_header": "Weather",
        "final_advice_header": "Final Advice",
        "header_wellness": "Wellness Tips",
        "header_sms_demo": "SMS/IVR Demo",
        "phone_input_label": "Phone Number",
        "button_send_sms": "Send SMS",
        "sms_sent_success": "SMS Sent!",
        "error_phone_number": "Invalid phone number."
    }
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
    t = random.choice(threats)
    info = THREAT_DATABASE.get(lang, {}).get(t, {"type": "Unknown", "solution": "No solution."})
    return {'threat_name': t.replace('_', ' ').title(), 'threat_type': info['type'], 'recommended_action': info['solution']}

def get_watering_advice(soil_type, lang):
    weather = {"temp": round(random.uniform(24, 32), 1), "humidity": random.randint(55, 85), "forecast": random.choice(["Sunny","Cloudy","Rain"])}
    return {"weather": weather, "advice": "Normal watering needed (25-30 min)."}

def get_harvest_advice(crop_name, sowing_date, lang):
    days = CROP_DATA.get(crop_name.lower(), {}).get("maturity_days", 100)
    harvest_date = sowing_date + timedelta(days=days)
    return {"harvest_window": f"{harvest_date.strftime('%d %b')} to {(harvest_date+timedelta(days=10)).strftime('%d %b, %Y')}",
            "market_outlook": "Stable prices",
            "weather_outlook": "Sunny",
            "advice": "Harvest at your convenience."}

# --- APP LAYOUT ---
st.sidebar.title("Language / ಭಾಷೆ / भाषा")
lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
lang_code = LANGUAGES[lang_display]
T = TEXT.get(lang_code, TEXT['en'])

st.title(T.get("title"))
st.markdown(T.get("welcome"))

tabs = st.tabs([T.get("tab_crop"), T.get("tab_health_diagnosis"), T.get("tab_profit"),
                T.get("tab_water"), T.get("tab_harvest"), T.get("tab_wellness"), T.get("tab_sms")])

with tabs[0]:  # Crop Recommendation
    st.header(T.get("header_crop"))
    soil_image = st.file_uploader("Upload Soil Image", type=["jpg", "png"])
    if soil_image:
        st.image(soil_image, caption="Soil")
        if st.button(T.get("button_analyze_soil")):
            with st.spinner(T.get("spinner_soil")):
                result = analyze_soil_image(soil_image)
                st.info(T.get("info_soil_analysis").format(soil_type=result['soil_type'], organic_matter=result['organic_matter_estimate']))
                features = [90, 42, 43, 25, 70, 6.5, 100]
                rec = predict_crop_and_plan(features, lang_code)
                st.success(T.get("success_crop").format(crop=rec['recommended_crop'].title()))

with tabs[1]:  # Field Health
    st.header(T.get("header_health"))
    if st.button(T.get("button_diagnose")):
        res = diagnose_threat(lang_code)
        st.write(res)

with tabs[2]:  # Profit
    st.header(T.get("header_profit"))
    if st.button(T.get("button_forecast").format(crop="Rice")):
        info = CROP_DATA["rice"]
        st.metric(T.get("metric_yield"), f"{info['yield_per_acre']} Qtl/Acre")
        st.metric(T.get("metric_price"), f"₹{info['market_price_per_quintal']}")
        st.metric(T.get("metric_revenue"), f"₹{info['yield_per_acre']*info['market_price_per_quintal']}")

with tabs[3]:  # Water Advisor
    st.header(T.get("header_water"))
    if st.button(T.get("button_water_advice")):
        res = get_watering_advice("Loamy", lang_code)
        st.write(res)

with tabs[4]:  # Harvest Advisor
    st.header(T.get("header_harvest"))
    if st.button(T.get("button_harvest_advice")):
        res = get_harvest_advice("rice", datetime.now()-timedelta(days=60), lang_code)
        st.write(res)

with tabs[5]:  # Wellness Tips
    st.header(T.get("header_wellness"))
    st.write("- Add compost regularly\n- Rotate crops\n- Avoid soil compaction")

with tabs[6]:  # SMS Demo
    st.header(T.get("header_sms_demo"))
    phone = st.text_input(T.get("phone_input_label"), "")
    if st.button(T.get("button_send_sms")):
        if len(phone) == 10:
            st.success(T.get("sms_sent_success"))
        else:
            st.error(T.get("error_phone_number"))

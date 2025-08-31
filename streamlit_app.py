# streamlit_app.py
# Final Corrected Version with Unique Button Keys

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
        base_dir = os.path.dirname(__file__)
        model_path = os.path.join(base_dir, "models", "crop_model.pkl")
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            return model
        else:
            st.warning("⚠️ crop_model.pkl not found in models/. Using fallback dummy model.")
            class DummyModel:
                def predict(self, X): return ["rice"]
            return DummyModel()
    except Exception as e:
        st.error(f"Fatal Error: Could not load crop_model.pkl → {e}")
        return None

crop_model = load_crop_model()

# --- KNOWLEDGE BASES (Multilingual Data) ---
CROP_ACTION_PLANS = {
    # ... unchanged ...
}
CROP_DATA = {
    # ... unchanged ...
}
THREAT_DATABASE = {
    # ... unchanged ...
}
TEXT = {
    # ... unchanged ...
}

# --- LANGUAGE MAPPING ---
LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi"
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
    n_diff, p_diff = 90 - data[0], 42 - data[1]
    rec_urea, rec_dap = 50 + (n_diff / 10) * 5, 50 + (p_diff / 10) * 2.5
    templates = {
        'en': f"- Your soil is {'low' if n_diff > 0 else 'high'} in Nitrogen. We recommend applying **{rec_urea:.1f} kg of Urea**.",
        'kn': f"- ನಿಮ್ಮ ಮಣ್ಣಿನಲ್ಲಿ ಸಾರಜನಕ {'ಕಡಿಮೆ' if n_diff > 0 else 'ಹೆಚ್ಚು'} ಇದೆ. ನಾವು **{rec_urea:.1f} ಕೆಜಿ ಯೂರಿಯಾ** ಬಳಸಲು ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ.",
        'hi': f"- आपकी मिट्टी में नाइट्रोजन {'कम' if n_diff > 0 else 'अधिक'} है। हम **{rec_urea:.1f} किलोग्राम यूरिया** डालने की सलाह देते हैं।"
    }
    action_plan["🌿 Personalized Fertilizer Plan"] = [templates[lang]]
    return {'recommended_crop': prediction_result, 'action_plan': action_plan}

def diagnose_threat(lang):
    threats = ["fall_armyworm", "leaf_blight", "amaranthus_viridis"]
    identified_threat_key = random.choice(threats)
    threat_info = THREAT_DATABASE.get(lang, {}).get(identified_threat_key, {"type": "Unknown", "solution": "No solution found."})
    return {'threat_name': identified_threat_key.replace('_', ' ').title(), 'threat_type': threat_info['type'], 'recommended_action': threat_info['solution']}

def get_watering_advice(soil_type, lang):
    weather = {"temp": round(random.uniform(24.0, 32.0), 1), "humidity": random.randint(55, 85), "forecast": random.choice(["Sunny", "Cloudy", "Light Haze", "Chance of Rain"])}
    advice_key = 'default'
    if "Rain" in weather['forecast']: advice_key = 'rain_expected'
    elif "Sandy" in soil_type and weather['temp'] > 28: advice_key = 'sandy_hot'
    elif "Clay" in soil_type and weather['temp'] < 26: advice_key = 'clay_cool'
    elif weather['temp'] > 30: advice_key = 'hot_day'
    templates = {
        'en': {'rain_expected': "NO watering needed. Rain is expected.", 'sandy_hot': "HIGH watering needed (45-60 min).", 'clay_cool': "LOW watering needed (15-20 min).", 'hot_day': "MODERATE watering needed (30-40 min).", 'default': "NORMAL watering needed (25-30 min)."},
        'kn': {'rain_expected': "ನೀರುಣಿಸುವ ಅಗತ್ಯವಿಲ್ಲ. ಮಳೆ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ.", 'sandy_hot': "ಹೆಚ್ಚು ನೀರುಣಿಸುವ ಅಗತ್ಯವಿದೆ (45-60 ನಿಮಿಷ).", 'clay_cool': "ಕಡಿಮೆ ನೀರುಣಿಸುವ ಅಗತ್ಯವಿದೆ (15-20 ನಿಮಿಷ).", 'hot_day': "ಮಧ್ಯಮ ನೀರುಣಿಸುವ ಅಗತ್ಯವಿದೆ (30-40 ನಿಮಿಷ).", 'default': "ಸಾಮಾನ್ಯ ನೀರುಣಿಸುವ ಅಗತ್ಯವಿದೆ (25-30 ನಿಮಿಷ)."},
        'hi': {'rain_expected': "पानी देने की आवश्यकता नहीं है। बारिश की उम्मीद है।", 'sandy_hot': "अधिक पानी देने की आवश्यकता है (45-60 मिनट)।", 'clay_cool': "कम पानी देने की आवश्यकता है (15-20 मिनट)।", 'hot_day': "मध्यम पानी देने की आवश्यकता है (30-40 मिनट)।", 'default': "सामान्य पानी देने की आवश्यकता है (25-30 मिनट)।"}
    }
    return {"weather": weather, "advice": templates.get(lang, templates['en']).get(advice_key)}

def get_harvest_advice(crop_name, sowing_date, lang):
    maturity_days = CROP_DATA.get(crop_name.lower(), {}).get("maturity_days", 100)
    harvest_date = sowing_date + timedelta(days=maturity_days)
    weather_forecast = random.choice(["Stable, sunny weather", "Risk of heavy rain in 5 days", "Clear skies, ideal conditions"])
    market_trend = random.choice(["Prices are stable", "Prices are trending up by 5-8%", "Prices are expected to dip slightly"])
    advice_key = 'default'
    if "rain" in weather_forecast.lower(): advice_key = 'harvest_now'
    elif "stable" in weather_forecast.lower() and "up" in market_trend.lower(): advice_key = 'wait'
    templates = {
        'en': {'harvest_now': "URGENT: Harvest within 3 days. Heavy rain is forecast, but current prices are high.", 'wait': "STRATEGIC: Hold your harvest for 5-7 days. Weather is stable and market prices are projected to rise.", 'default': "STANDARD: Your crop is ready. Harvest at your convenience as weather and market conditions are stable."},
        'kn': {'harvest_now': "ತುರ್ತು: 3 ದಿನಗಳಲ್ಲಿ ಕೊಯ್ಲು ಮಾಡಿ. ಭಾರೀ ಮಳೆಯ ಮುನ್ಸೂಚನೆ ಇದೆ, ಆದರೆ ಪ್ರಸ್ತುತ ಬೆಲೆಗಳು ಹೆಚ್ಚಿವೆ.", 'wait': "ಕಾರ್ಯತಂತ್ರ: ನಿಮ್ಮ ಕೊಯ್ಲನ್ನು 5-7 ದಿನಗಳವರೆಗೆ ಹಿಡಿದುಕೊಳ್ಳಿ. ವಾತಾವರಣ ಸ್ಥಿರವಾಗಿದೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ಏರುವ ನಿರೀಕ್ಷೆಯಿದೆ.", 'default': "ಪ್ರಮಾಣಿತ: ನಿಮ್ಮ ಬೆಳೆ ಸಿದ್ಧವಾಗಿದೆ. ಹವಾಮಾನ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಪರಿಸ್ಥಿತಿಗಳು ಸ್ಥಿರವಾಗಿರುವುದರಿಂದ ನಿಮ್ಮ ಅನುಕೂಲಕ್ಕೆ ತಕ್ಕಂತೆ ಕೊಯ್ಲು ಮಾಡಿ."},
        'hi': {'harvest_now': "अत्यावश्यक: 3 दिनों के भीतर कटाई करें। भारी बारिश का पूर्वानुमान है, लेकिन मौजूदा कीमतें ऊंची हैं।", 'wait': "रणनीतिक: अपनी फसल को 5-7 दिनों के लिए रोक कर रखें। मौसम स्थिर है और बाजार की कीमतों में वृद्धि का अनुमान है।", 'default': "मानक: आपकी फसल तैयार है। मौसम और बाजार की स्थिति स्थिर होने के कारण अपनी सुविधानुसार कटाई करें।"}
    }
    return {"harvest_window": f"{harvest_date.strftime('%d %b')} to {(harvest_date + timedelta(days=10)).strftime('%d %b, %Y')}", "market_outlook": market_trend, "weather_outlook": weather_forecast, "advice": templates.get(lang, templates['en']).get(advice_key)}

# --- APP LAYOUT ---
if crop_model is None:
    st.error("Fatal Error: Crop recommendation model not found in `models/crop_model.pkl`. Please ensure the file exists in your repo.")
else:
    st.sidebar.title("Language / ಭಾಷೆ / भाषा")
    lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_display]
    T = TEXT.get(lang_code, TEXT['en'])

    st.title(T.get("title", "SmartAgro AI"))
    st.markdown(T.get("welcome", "Welcome!"))

    tabs = st.tabs([T.get("tab_crop", "Crop Recommendation"),
                    T.get("tab_health_diagnosis", "Field Health Diagnosis"),
                    T.get("tab_profit", "Profit Forecast"),
                    T.get("tab_water", "Water Advisor"),
                    T.get("tab_harvest", "Harvest Advisor"),
                    T.get("tab_wellness", "Wellness Tips"),
                    T.get("tab_sms", "SMS/IVR Demo")])

    with tabs[0]:
        if st.button(T.get("button_analyze_soil", "Analyze Soil"), key="analyze_soil_btn"):
            pass

    with tabs[1]:
        if st.button(T.get("button_diagnose", "Diagnose"), key="diagnose_btn"):
            pass

    with tabs[2]:
        if st.button(T.get("button_forecast", "Forecast"), key="forecast_btn"):
            pass

    with tabs[3]:
        if st.button(T.get("button_water_advice", "Water Advice"), key="water_btn"):
            pass

    with tabs[4]:
        if st.button(T.get("button_harvest_advice", "Harvest Advice"), key="harvest_btn"):
            pass

    with tabs[6]:
        if st.button(T.get("button_send_sms", "Send SMS"), key="sms_btn"):
            pass

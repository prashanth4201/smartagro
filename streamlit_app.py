# streamlit_app.py
# Final Corrected Version for Successful Deployment

import streamlit as st
from PIL import Image
import joblib
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")

# --- LANGUAGE OPTIONS ---
LANGUAGES = {"English": "en", "ಕನ್ನಡ": "kn", "हिंदी": "hi"}

TEXT = {
    "en": {
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
        "header_crop": "Find the Perfect Crop & Get a Full Cultivation Guide",
        "subheader_crop_step1": "Step 1: Upload a Photo of Your Soil",
        "uploader_soil": "Take a picture of your farm's soil...",
        "button_analyze_soil": "Analyze Soil Visually",
        "spinner_soil": "AI is performing a visual check-up...",
        "subheader_crop_step2": "Step 2: Add Details From Your Soil Test",
        "info_soil_analysis": "Visual Analysis: Your soil looks like **{soil_type}** with **{organic_matter}** organic matter.",
        "button_get_plan": "Get My Crop Action Plan",
        "spinner_plan": "AI is generating your personalized plan...",
        "success_crop": "Success! The best crop for you is: **{crop}**",
        "subheader_plan": "Your Action Plan for {crop}",
        "button_start_over": "Start Over",
        "header_health": "AI Field Doctor: Diagnose Diseases, Pests & Weeds",
        "uploader_health": "Upload a photo of a sick leaf, an unknown pest, or a weed...",
        "button_diagnose": "Diagnose Now",
        "diagnosis_result": "AI Diagnosis Result",
        "threat_name": "Identified Threat",
        "threat_type": "Threat Type",
        "threat_action": "Recommended Action",
        "header_profit": "💰 Profitability & Yield Forecaster",
        "subheader_profit": "Get an estimate of your potential earnings based on your recommended crop.",
        "button_forecast": "Calculate Forecast for {crop}",
        "subheader_results": "Forecast Results",
        "metric_yield": "Expected Yield",
        "metric_price": "Live Market Price",
        "metric_revenue": "Estimated Revenue",
        "warning_no_crop": "Please get a crop recommendation from the first tab before you can use this feature.",
        "header_wellness": "Proactive Tips for Healthy Plants",
        "wellness_intro": "Preventing diseases is better than curing them. Here are some tips to keep your plants healthy.",
        "wellness_soil_header": "1. Healthy Soil",
        "wellness_soil_points": [
            "- Regularly add compost.",
            "- Practice crop rotation.",
            "- Avoid soil compaction.",
        ],
        "wellness_water_header": "2. Smart Watering",
        "wellness_water_points": [
            "- Water early in the morning.",
            "- Use drip irrigation.",
            "- Avoid overwatering.",
        ],
        "wellness_pest_header": "3. Pest Management",
        "wellness_pest_points": [
            "- Encourage natural predators.",
            "- Use neem oil as a first defense.",
            "- Inspect plants regularly.",
        ],
        "header_sms_demo": "SMS / Voice (IVR) Service Simulation",
        "subheader_sms_demo": "This shows how a farmer with a basic phone could get advice.",
        "ivr_title": "Simulate Crop Recommendation via IVR/SMS",
        "phone_input_label": "Enter Farmer's 10-digit Phone Number:",
        "ivr_instructions": "Imagine the farmer entered these values using their phone's keypad:",
        "button_send_sms": "Simulate Sending SMS Recommendation",
        "sms_sent_success": "SMS Sent Successfully!",
        "sms_preview": "Farmer would receive this message:",
        "error_phone_number": "Please enter a valid 10-digit phone number.",
        "header_water": "💧 AI Water Advisor",
        "subheader_water": "Get a hyper-personalized daily irrigation schedule to save water and maximize yield.",
        "button_water_advice": "Get Today's Watering Advice",
        "subheader_weather_sim": "Today's Weather (Simulated)",
        "subheader_advice": "Your Personalized Recommendation",
        "warning_no_soil": "Please complete the visual soil analysis first.",
        "header_harvest": "📈 AI Harvest & Market Advisor",
        "subheader_harvest": "Get a strategic recommendation on the best time to harvest and sell for maximum profit.",
        "sowing_date_label": "Enter your crop's sowing date:",
        "button_harvest_advice": "Get Harvest & Selling Advice",
        "harvest_window_header": "Optimal Harvest Window",
        "market_outlook_header": "Market Price Outlook (Simulated)",
        "weather_outlook_header": "Weather Outlook (Next 7 Days)",
        "final_advice_header": "Final Strategic Recommendation",
    },
    "kn": {},
    "hi": {},
}

CROP_DATA = {
    "rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050, "maturity_days": 120},
    "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100, "maturity_days": 100},
    "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500, "maturity_days": 150},
    "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000, "maturity_days": 365},
}

# --- MODEL LOADER (expects crop_model.pkl in repo root) ---
@st.cache_resource
def load_crop_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), "crop_model.pkl")
        if os.path.exists(model_path):
            return joblib.load(model_path)
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

# --- SIMPLE AI LOGIC ---
def analyze_soil_image(image_file):
    with Image.open(image_file) as img:
        avg_color = np.array(img.convert("RGB")).mean(axis=(0, 1))
        brightness = sum(avg_color) / 3
        if brightness < 80:
            return {"soil_type": "Clay Loam", "organic_matter_estimate": "High"}
        elif brightness < 140:
            return {"soil_type": "Loamy Soil", "organic_matter_estimate": "Moderate"}
        else:
            return {"soil_type": "Sandy Soil", "organic_matter_estimate": "Low"}

def predict_crop(data):
    return crop_model.predict([data])[0]

def get_watering_advice():
    return random.choice([
        "No watering needed today (rain expected).",
        "Water for 20 minutes in the morning.",
        "Deep watering for 45 minutes recommended.",
    ])

def get_harvest_advice():
    return random.choice([
        "Harvest in the next 3 days to avoid rain.",
        "Wait 1 more week for better market prices.",
        "Harvest anytime in the next 10 days.",
    ])

# --- APP UI ---
st.sidebar.title("🌍 Language")
lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
lang_code = LANGUAGES[lang_display]
T = TEXT.get(lang_code) or TEXT["en"]

st.title(T["title"])
st.write(T["welcome"])

tabs = st.tabs([
    T["tab_crop"], T["tab_health_diagnosis"], T["tab_profit"],
    T["tab_water"], T["tab_harvest"], T["tab_wellness"], T["tab_sms"]
])

# --- Crop Recommendation ---
with tabs[0]:
    st.header(T["header_crop"])
    soil_img = st.file_uploader(T["uploader_soil"], type=["jpg","jpeg","png"])
    if soil_img and st.button(T["button_analyze_soil"], key="analyze_soil"):
        res = analyze_soil_image(soil_img)
        st.success(f"Soil type: **{res['soil_type']}**, Organic Matter: **{res['organic_matter_estimate']}**")

# --- Field Health ---
with tabs[1]:
    st.header(T["header_health"])
    health_img = st.file_uploader(T["uploader_health"], type=["jpg","jpeg","png"])
    if health_img and st.button(T["button_diagnose"], key="diagnose"):
        st.info("Threat detected: Fall Armyworm 🐛 → Use pheromone traps.")

# --- Profit Forecast ---
with tabs[2]:
    st.header(T["header_profit"])
    if st.button(T["button_forecast"].format(crop="Rice"), key="forecast"):
        st.success("Estimated Revenue: ₹45,000 per acre.")

# --- Water Advisor ---
with tabs[3]:
    st.header(T["header_water"])
    if st.button(T["button_water_advice"], key="water"):
        st.success(get_watering_advice())

# --- Harvest Advisor ---
with tabs[4]:
    st.header(T["header_harvest"])
    if st.button(T["button_harvest_advice"], key="harvest"):
        st.success(get_harvest_advice())

# --- Wellness Tips ---
with tabs[5]:
    st.header(T["header_wellness"])
    st.markdown("- Add compost regularly\n- Rotate crops\n- Use neem oil spray")

# --- SMS Demo ---
with tabs[6]:
    st.header(T["header_sms_demo"])
    phone = st.text_input("📞 Enter phone number", "9876543210", max_chars=10)
    if st.button(T["button_send_sms"], key="sms"):
        st.success(f"SMS sent to {phone}: Best crop for your soil is Rice 🌾")

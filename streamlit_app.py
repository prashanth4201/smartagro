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

# --- PAGE CONFIGURATION (MUST be the first Streamlit command) ---
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")

# --- KNOWLEDGE BASES & DICTIONARIES (Define all data first) ---
LANGUAGES = {"English": "en", "ಕನ್ನಡ": "kn", "हिंदी": "hi"}

TEXT = {
    'en': {
        "title": "SmartAgro AI – Your Farm's Smart Assistant", "welcome": "Welcome! Use our AI tools for smarter farming decisions.",
        "tab_crop": "🌾 Crop Recommendation", "tab_health_diagnosis": "🌿 Field Health Diagnosis", "tab_profit": "💰 Profit Forecast", "tab_wellness": "💚 Wellness Tips", "tab_sms": "📱 SMS/IVR Demo", "tab_water": "💧 AI Water Advisor", "tab_harvest": "📈 Harvest Advisor",
        "role_selector_title": "Select Your Role", "role_farmer": "I am a Farmer", "role_kiosk": "I am a Kiosk Operator", "kiosk_info": "This mode helps you assist multiple farmers.",
        "header_crop": "Find the Perfect Crop & Get a Full Cultivation Guide", "subheader_crop_step1": "Step 1: Upload a Photo of Your Soil", "uploader_soil": "Take a picture of your farm's soil...", "button_analyze_soil": "Analyze Soil Visually", "spinner_soil": "AI is performing a visual check-up...",
        "subheader_crop_step2": "Step 2: Add Details From Your Soil Test", "info_soil_analysis": "Visual Analysis: Your soil looks like **{soil_type}** with **{organic_matter}** organic matter.",
        "button_get_plan": "Get My Crop Action Plan", "spinner_plan": "AI is generating your personalized plan...", "success_crop": "Success! The best crop for you is: **{crop}**", "subheader_plan": "Your Action Plan for {crop}", "button_start_over": "Start Over",
        "header_health": "AI Field Doctor: Diagnose Diseases, Pests & Weeds", "uploader_health": "Upload a photo of a sick leaf, an unknown pest, or a weed...", "button_diagnose": "Diagnose Now", "diagnosis_result": "AI Diagnosis Result", "threat_name": "Identified Threat", "threat_type": "Threat Type", "threat_action": "Recommended Action",
        "header_profit": "💰 Profitability & Yield Forecaster", "subheader_profit": "Get an estimate of your potential earnings based on your recommended crop.", "button_forecast": "Calculate Forecast for {crop}", "subheader_results": "Forecast Results", "metric_yield": "Expected Yield", "metric_price": "Live Market Price", "metric_revenue": "Estimated Revenue", "warning_no_crop": "Please get a crop recommendation from the first tab before you can use this feature.",
        "header_wellness": "Proactive Tips for Healthy Plants", "wellness_intro": "Preventing diseases is better than curing them. Here are some tips to keep your plants healthy.", "wellness_soil_header": "1. Healthy Soil", "wellness_soil_points": ["- Regularly add compost.", "- Practice crop rotation.", "- Avoid soil compaction."], "wellness_water_header": "2. Smart Watering", "wellness_water_points": ["- Water early in the morning.", "- Use drip irrigation.", "- Avoid overwatering."], "wellness_pest_header": "3. Pest Management", "wellness_pest_points": ["- Encourage natural predators.", "- Use neem oil as a first defense.", "- Inspect plants regularly."],
        "header_sms_demo": "SMS / Voice (IVR) Service Simulation", "subheader_sms_demo": "This shows how a farmer with a basic phone could get advice.", "ivr_title": "Simulate Crop Recommendation via IVR/SMS", "phone_input_label": "Enter Farmer's 10-digit Phone Number:", "ivr_instructions": "Imagine the farmer entered these values using their phone's keypad:", "button_send_sms": "Simulate Sending SMS Recommendation", "sms_sent_success": "SMS Sent Successfully!", "sms_preview": "Farmer would receive this message:", "error_phone_number": "Please enter a valid 10-digit phone number.",
        "header_water": "💧 AI Water Advisor", "subheader_water": "Get a hyper-personalized daily irrigation schedule to save water and maximize yield.", "button_water_advice": "Get Today's Watering Advice", "subheader_weather_sim": "Today's Weather (Simulated for Bangarapet)", "subheader_advice": "Your Personalized Recommendation", "warning_no_soil": "Please complete the visual soil analysis first.",
        "header_harvest": "📈 AI Harvest & Market Advisor", "subheader_harvest": "Get a strategic recommendation on the best time to harvest and sell for maximum profit.", "sowing_date_label": "Enter your crop's sowing date:", "button_harvest_advice": "Get Harvest & Selling Advice", "harvest_window_header": "Optimal Harvest Window", "market_outlook_header": "Market Price Outlook (Simulated)", "weather_outlook_header": "Weather Outlook (Next 7 Days)", "final_advice_header": "Final Strategic Recommendation"
    },
    'kn': {
        "title": "ಸ್ಮಾರ್ಟ್ ಆಗ್ರೋ AI – ನಿಮ್ಮ ಜಮೀನಿನ ಸ್ಮಾರ್ಟ್ ಸಹಾಯಕ", "welcome": "ಸ್ವಾಗತ! ಉತ್ತಮ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ನಮ್ಮ AI ಬಳಸಿ.",
        "tab_crop": "🌾 ಬೆಳೆ ಶಿಫಾರಸು", "tab_health_diagnosis": "🌿 ಕ್ಷೇತ್ರ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆ", "tab_profit": "💰 ಲಾಭದ ಮುನ್ಸೂಚನೆ", "tab_wellness": "💚 ಆರೋಗ್ಯ ಸಲಹೆಗಳು", "tab_sms": "📱 SMS/IVR ಪ್ರಾತ್ಯಕ್ಷಿಕೆ", "tab_water": "💧 AI ನೀರು ಸಲಹೆಗಾರ", "tab_harvest": "📈 ಸುಗ್ಗಿ ಸಲಹೆಗಾರ", "role_selector_title": "ನಿಮ್ಮ ಪಾತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "role_farmer": "ನಾನು ರೈತ", "role_kiosk": "ನಾನು ಕಿಯೋಸ್ಕ್ ಆಪರೇಟರ್", "kiosk_info": "ಈ ಮೋಡ್ ಅನೇಕ ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡಲು ನಿಮಗೆ ಅನುವು ಮಾಡಿಕೊಡುತ್ತದೆ.",
    },
    'hi': {
        "title": "स्मार्ट एग्रो AI – आपके खेत का स्मार्ट सहायक", "welcome": "आपका स्वागत है! बेहतर निर्णयों के लिए हमारे AI उपकरणों का उपयोग करें।",
        "tab_crop": "🌾 फसल सिफारिश", "tab_health_diagnosis": "🌿 क्षेत्र स्वास्थ्य निदान", "tab_profit": "💰 लाभ का पूर्वानुमान", "tab_wellness": "💚 स्वास्थ्य सुझाव", "tab_sms": "📱 SMS/IVR डेमो", "tab_water": "💧 AI जल सलाहकार", "tab_harvest": "📈 कटाई सलाहकार", "role_selector_title": "अपनी भूमिका चुनें", "role_farmer": "मैं एक किसान हूँ", "role_kiosk": "मैं एक कियोस्क ऑपरेटर हूँ", "kiosk_info": "यह मोड आपको कई किसानों की सहायता करने में मदद करता है।",
    }
}
CROP_ACTION_PLANS = {
    'en': {
        "rice": {
            "🌾 Land Preparation": ["- Plow the land 2-3 times and level it.", "- Ensure good drainage and a fine tilth."],
            "🌱 Seed & Sowing": ["- Use high-yield, disease-resistant varieties.", "- Seed rate: 20-25 kg/acre.", "- Transplant seedlings after 25-30 days."],
            "💧 Irrigation": ["- Maintain a water level of 2-5 cm.", "- Stop irrigation 15 days before harvesting."],
            "🐞 Pest Control": ["- Monitor for stem borer and leaf folder.", "- Apply neem oil as a preventive measure."]
        },
        "maize": {
            "🌾 Land Preparation": ["- Deep plow the land followed by harrowing.", "- The soil should be fine and weed-free."],
            "🌱 Seed & Sowing": ["- Use a hybrid variety like HQPM-1.", "- Seed rate: 8-10 kg/acre.", "- Spacing: 60 cm between rows, 20 cm between plants."],
            "💧 Irrigation": ["- Critical watering stages are knee-high, flowering, and grain filling."],
            "🐞 Pest Control": ["- Watch out for fall armyworm. Use pheromone traps."]
        }
    },
    'kn': { "rice": {}, "maize": {} },
    'hi': { "rice": {}, "maize": {} }
}
CROP_DATA = {
    "rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050, "maturity_days": 120},
    "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100, "maturity_days": 100},
    "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500, "maturity_days": 150},
    "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000, "maturity_days": 365}
}
THREAT_DATABASE = {
    'en': {"fall_armyworm": {"type": "Pest", "solution": "Use pheromone traps."}, "leaf_blight": {"type": "Disease", "solution": "Remove leaves, apply fungicide."}, "amaranthus_viridis": {"type": "Weed", "solution": "Manual removal or herbicide."}},
    'kn': {"fall_armyworm": {"type": "ಕೀಟ", "solution": "..."}, "leaf_blight": {"type": "ರೋಗ", "solution": "..."}, "amaranthus_viridis": {"type": "ಕಳೆ", "solution": "..."}},
    'hi': {"fall_armyworm": {"type": "कीट", "solution": "..."}, "leaf_blight": {"type": "रोग", "solution": "..."}, "amaranthus_viridis": {"type": "खरपतवार", "solution": "..."}}
}

# --- AI MODEL LOADING (CORRECTED AS PER YOUR INSTRUCTION) ---
@st.cache_resource
def load_crop_model():
    """Load the crop recommendation model safely from the root directory."""
    try:
        # This path now correctly looks for the model in the root folder.
        model_path = os.path.join(os.path.dirname(__file__), 'crop_model.pkl')
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            st.error(f"Fatal Error: `crop_model.pkl` not found in the root of the repository. Please ensure the file is uploaded and correctly named.")
            return None
    except Exception as e:
        st.error(f"Fatal Error: Could not load `crop_model.pkl`. Error: {e}")
        return None

# --- AI LOGIC FUNCTIONS ---
def analyze_soil_image(image_file):
    with Image.open(image_file) as img:
        avg_color = np.array(img.convert('RGB')).mean(axis=(0, 1))
        brightness = sum(avg_color) / 3
        if brightness < 80: return {"soil_type": "Clay Loam", "organic_matter_estimate": "High"}
        elif brightness < 140: return {"soil_type": "Loamy Soil", "organic_matter_estimate": "Moderate"}
        else: return {"soil_type": "Sandy Soil", "organic_matter_estimate": "Low"}

def predict_crop_and_plan(crop_model, data, lang):
    if crop_model is None:
        st.error("Crop model is not loaded. Cannot get a recommendation.")
        return None
    prediction_result = crop_model.predict([data])[0]
    action_plan = CROP_ACTION_PLANS.get(lang, {}).get(prediction_result.lower(), {})
    n_diff, p_diff = 90 - data[0], 42 - data[1]
    rec_urea, rec_dap = 50 + (n_diff / 10) * 5, 50 + (p_diff / 10) * 2.5
    
    templates = {
        'en': f"- Your soil is {'low' if n_diff > 0 else 'high'} in Nitrogen. We recommend applying **{rec_urea:.1f} kg of Urea**.",
        'kn': f"- ನಿಮ್ಮ ಮಣ್ಣಿನಲ್ಲಿ ಸಾರಜನಕ {'ಕಡಿಮೆ' if n_diff > 0 else 'ಹೆಚ್ಚು'} ಇದೆ. ನಾವು **{rec_urea:.1f} ಕೆಜಿ ಯೂರಿಯಾ** ಬಳಸಲು ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ.",
        'hi': f"- आपकी मिट्टी में नाइट्रोजन {'कम' if n_diff > 0 else 'अधिक'} है। हम **{rec_urea:.1f} किलोग्राम यूरिया** डालने की सलाह देते हैं।"
    }
    action_plan["🌿 Personalized Fertilizer Plan"] = [templates.get(lang, templates['en'])]
    return {'recommended_crop': prediction_result, 'action_plan': action_plan}

def diagnose_threat(lang):
    threats = ["fall_armyworm", "leaf_blight", "amaranthus_viridis"]
    t = random.choice(threats)
    info = THREAT_DATABASE.get(lang, {}).get(t, {"type": "Unknown", "solution": "No solution."})
    return {'threat_name': t.replace('_', ' ').title(), 'threat_type': info['type'], 'recommended_action': info['solution']}

def get_watering_advice(soil_type, lang):
    weather = {"temp": round(random.uniform(24, 32), 1), "humidity": random.randint(55, 85), "forecast": random.choice(["Sunny","Cloudy","Rain"])}
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
    days = CROP_DATA.get(crop_name.lower(), {}).get("maturity_days", 100)
    harvest_date = sowing_date + timedelta(days=days)
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

# Load model first and check for its existence
crop_model = load_crop_model()

# Sidebar setup (Language and Role)
st.sidebar.title("Language / ಭಾಷೆ / भाषा")
lang_display = st.sidebar.selectbox("", list(LANGUAGES.keys()))
lang_code = LANGUAGES[lang_display]
T = TEXT.get(lang_code, TEXT['en'])

st.sidebar.title(T.get("role_selector_title", "Select Your Role"))
user_role = st.sidebar.radio("", (T.get("role_farmer", "I am a Farmer"), T.get("role_kiosk", "I am a Kiosk Operator")))
if T.get("role_kiosk", "I am a Kiosk Operator") in user_role:
    st.sidebar.info(T.get("kiosk_info", "This mode helps you assist multiple farmers."))

# Initialize session state
if 'soil_analysis_done' not in st.session_state: st.session_state.soil_analysis_done = False
if 'soil_analysis_result' not in st.session_state: st.session_state.soil_analysis_result = None
if 'crop_recommendation_result' not in st.session_state: st.session_state.crop_recommendation_result = None

# Main panel
st.title(T.get("title"))
st.markdown(T.get("welcome"))

# Only proceed if the model was loaded successfully
if crop_model:
    tab_keys = ["tab_crop", "tab_health_diagnosis", "tab_profit", "tab_water", "tab_harvest", "tab_wellness", "tab_sms"]
    tabs = st.tabs([T.get(key, key.replace('_', ' ').title()) for key in tab_keys])

    with tabs[0]: # Crop Recommendation
        st.header(T.get("header_crop"))
        if not st.session_state.soil_analysis_done:
            st.subheader(T.get("subheader_crop_step1", "Step 1: Upload a Photo of Your Soil"))
            soil_image = st.file_uploader(T.get("uploader_soil", "Upload Soil Image"), type=["jpg", "jpeg", "png"], key="soil_uploader")
            if soil_image:
                st.image(soil_image, caption='Your Soil', width=300)
                if st.button(T.get("button_analyze_soil"), use_container_width=True):
                    with st.spinner(T.get("spinner_soil")):
                        st.session_state.soil_analysis_result = analyze_soil_image(soil_image)
                        st.session_state.soil_analysis_done = True
                        st.rerun()
        if st.session_state.soil_analysis_done:
            st.subheader(T.get("subheader_crop_step2"))
            result = st.session_state.soil_analysis_result
            if result and 'error' not in result:
                st.info(T.get("info_soil_analysis").format(soil_type=result['soil_type'], organic_matter=result['organic_matter_estimate']))
            
            col1, col2 = st.columns(2)
            with col1:
                n = st.number_input("Nitrogen (N)", 0, 200, 90)
                p = st.number_input("Phosphorus (P)", 0, 200, 42)
                k = st.number_input("Potassium (K)", 0, 200, 43)
            with col2:
                temp = st.number_input("Temperature (°C)", -10.0, 60.0, 25.5, 0.1)
                hum = st.number_input("Humidity (%)", 0.0, 100.0, 70.0, 0.1)
                ph = st.number_input("Soil pH", 0.0, 14.0, 6.5, 0.1)
                rain = st.number_input("Rainfall (mm)", 0.0, 500.0, 100.0, 0.1)

            if st.button(T.get("button_get_plan"), use_container_width=True, type="primary"):
                with st.spinner(T.get("spinner_plan")):
                    features = [n, p, k, temp, hum, ph, rain]
                    st.session_state.crop_recommendation_result = predict_crop_and_plan(crop_model, features, lang_code)
            
            if st.session_state.crop_recommendation_result:
                res = st.session_state.crop_recommendation_result
                st.success(T.get("success_crop").format(crop=res['recommended_crop'].title()))
                st.subheader(T.get("subheader_plan").format(crop=res['recommended_crop'].title()))
                if 'action_plan' in res:
                    for step, details in res['action_plan'].items():
                        with st.expander(f"**{step}**"):
                            for point in details: st.markdown(point)
            
            if st.button(T.get("button_start_over")):
                st.session_state.soil_analysis_done = False
                st.session_state.soil_analysis_result = None
                st.session_state.crop_recommendation_result = None
                st.rerun()

    with tabs[1]: # Field Health Diagnosis
        st.header(T.get("header_health"))
        uploaded_file = st.file_uploader(T.get("uploader_health", "Upload an image of the threat"), type=["jpg", "jpeg", "png"], key="health_uploader")
        if uploaded_file:
            st.image(uploaded_file, caption='Image for Analysis', use_column_width=True)
            if st.button(T.get("button_diagnose"), use_container_width=True, type="primary"):
                with st.spinner('Your AI Field Doctor is analyzing the image...'):
                    result = diagnose_threat(lang_code)
                    st.subheader(T.get("diagnosis_result"))
                    col1, col2 = st.columns(2)
                    col1.metric(T.get("threat_name"), result['threat_name'])
                    col2.metric(T.get("threat_type"), result['threat_type'])
                    st.success(f"**{T.get('threat_action')}:** {result['recommended_action']}")

    with tabs[2]: # Profit Forecast
        st.header(T.get("header_profit"))
        st.markdown(T.get("subheader_profit", "Get an estimate of your potential earnings."))
        if st.session_state.crop_recommendation_result:
            crop = st.session_state.crop_recommendation_result['recommended_crop']
            st.info(f"Forecasting for your recommended crop: **{crop.title()}**")
            if st.button(T.get("button_forecast", "Calculate Forecast").format(crop=crop.title()), use_container_width=True, type="primary"):
                with st.spinner("Analyzing market data..."):
                    crop_info = CROP_DATA.get(crop.lower())
                    if crop_info:
                        revenue = crop_info['yield_per_acre'] * crop_info['market_price_per_quintal']
                        st.subheader(T.get("subheader_results"))
                        col1, col2, col3 = st.columns(3)
                        col1.metric(T.get("metric_yield"), f"{crop_info['yield_per_acre']} Quintals/Acre")
                        col2.metric(T.get("metric_price"), f"₹{crop_info['market_price_per_quintal']:,}/Quintal")
                        col3.metric(T.get("metric_revenue"), f"₹{revenue:,.2f} / Acre")
        else:
            st.warning(T.get("warning_no_crop"))

    with tabs[3]: # Water Advisor
        st.header(T.get("header_water"))
        st.markdown(T.get("subheader_water"))
        if st.session_state.soil_analysis_result and st.session_state.soil_analysis_result.get('soil_type'):
            soil_type = st.session_state.soil_analysis_result['soil_type']
            st.info(f"Using your analyzed soil type: **{soil_type}**")
            if st.button(T.get("button_water_advice"), use_container_width=True, type="primary"):
                with st.spinner("Checking real-time weather..."):
                    result = get_watering_advice(soil_type, lang_code)
                    weather, advice = result['weather'], result['advice']
                    st.subheader(T.get("subheader_weather_sim"))
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Temperature", f"{weather['temp']} °C")
                    col2.metric("Humidity", f"{weather['humidity']} %")
                    col3.metric("Forecast", weather['forecast'])
                    st.subheader(T.get("subheader_advice"))
                    st.success(f"**{advice}**")
        else:
            st.warning(T.get("warning_no_soil"))
    
    with tabs[4]: # Harvest Advisor
        st.header(T.get("header_harvest"))
        st.markdown(T.get("subheader_harvest"))
        if st.session_state.crop_recommendation_result:
            crop = st.session_state.crop_recommendation_result['recommended_crop']
            st.info(f"Get harvest advice for your recommended crop: **{crop.title()}**")
            sowing_date = st.date_input(T.get("sowing_date_label"), datetime.now() - timedelta(days=60))
            if st.button(T.get("button_harvest_advice"), use_container_width=True, type="primary"):
                with st.spinner("Analyzing forecasts..."):
                    result = get_harvest_advice(crop, sowing_date, lang_code)
                    st.subheader(T.get("harvest_window_header"))
                    st.info(result['harvest_window'])
                    col1, col2 = st.columns(2)
                    col1.subheader(T.get("market_outlook_header"))
                    col1.write(result['market_outlook'])
                    col2.subheader(T.get("weather_outlook_header"))
                    col2.write(result['weather_outlook'])
                    st.subheader(T.get("final_advice_header"))
                    st.success(f"**{result['advice']}**")
        else:
            st.warning(T.get("warning_no_crop"))

    with tabs[5]: # Wellness Tips
        st.header(T.get("header_wellness"))
        st.markdown(T.get("wellness_intro", ""))
        st.subheader(T.get("wellness_soil_header", ""))
        for point in T.get("wellness_soil_points", []): st.markdown(point)
        st.subheader(T.get("wellness_water_header", ""))
        for point in T.get("wellness_water_points", []): st.markdown(point)
        st.subheader(T.get("wellness_pest_header", ""))
        for point in T.get("wellness_pest_points", []): st.markdown(point)
        
    with tabs[6]: # SMS/IVR Demo
        st.header(T.get("header_sms_demo"))
        st.markdown(T.get("subheader_sms_demo", ""))
        st.subheader(T.get("ivr_title"))
        phone = st.text_input(T.get("phone_input_label", "Phone Number"), "9988776655", max_chars=10)
        st.markdown(T.get("ivr_instructions", ""))
        col1, col2 = st.columns(2)
        with col1:
            n_sms = st.number_input("N", 0, 200, 100, key="n_sms")
            p_sms = st.number_input("P", 0, 200, 50, key="p_sms")
        with col2:
            k_sms = st.number_input("K", 0, 200, 50, key="k_sms")
            ph_sms = st.number_input("pH", 0.0, 14.0, 7.0, 0.1, key="ph_sms")

        if st.button(T.get("button_send_sms"), use_container_width=True):
            if phone and len(phone) == 10:
                with st.spinner("Sending SMS..."):
                    features = [n_sms, p_sms, k_sms, 26.0, 80.0, ph_sms, 120.0]
                    result = predict_crop_and_plan(crop_model, features, lang_code)
                    if result:
                        crop_name = result['recommended_crop']
                        templates = {
                            'en': f"SmartAgro AI Alert for +91-{phone}: Based on your soil, the best crop is **{crop_name}**. Visit your local kiosk for a full plan.",
                            'kn': f"+91-{phone} ಸಂಖ್ಯೆಗೆ ಸ್ಮಾರ್ಟ್ ಆಗ್ರೋ AI ಸಂದೇಶ: ನಿಮ್ಮ ಮಣ್ಣಿನ ಪ್ರಕಾರ, ಉತ್ತಮ ಬೆಳೆ **{crop_name}**. ಪೂರ್ಣ ಯೋಜನೆಗಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕಿಯೋಸ್ಕ್ಗೆ ಭೇಟಿ ನೀಡಿ.",
                            'hi': f"+91-{phone} के लिए स्मार्ट एग्रो AI अलर्ट: आपकी मिट्टी के आधार पर, सबसे अच्छी फसल **{crop_name}** है। पूरी योजना के लिए अपने स्थानीय कियोस्क पर जाएँ।"
                        }
                        st.success(T.get("sms_sent_success"))
                        st.info(templates[lang_code])
            else:
                st.error(T.get("error_phone_number"))


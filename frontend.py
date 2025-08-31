# frontend.py

import streamlit as st
import requests
from PIL import Image
from datetime import date, timedelta

# --- PAGE CONFIGURATION & TEXT (FULLY TRANSLATED) ---
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")
LANGUAGES = {"English": "en", "ಕನ್ನಡ": "kn", "हिंदी": "hi"}
TEXT = {
    'en': {
        "title": "SmartAgro AI – Your Farm's Smart Assistant", "welcome": "Welcome! Use AI for smarter farming decisions.",
        "tab_crop": "🌾 Crop Plan", "tab_health": "🔬 Field Doctor", "tab_profit": "💰 Profit Forecast", "tab_harvest": "📈 Harvest Advisor", "tab_water": "💧 Water Advisor", "tab_wellness": "💚 Wellness Tips", "tab_sms": "📱 SMS Demo",
        "role_selector_title": "Select Your Role", "role_farmer": "I am a Farmer", "role_kiosk": "I am a Kiosk Operator", "kiosk_info": "This mode helps you assist multiple farmers.",
        "header_crop": "Get Your Complete Crop Action Plan", "subheader_crop_step1": "Step 1: Upload Soil Photo", "uploader_soil": "Take a picture of your farm's soil...", "button_analyze_soil": "Analyze Soil Visually",
        "subheader_crop_step2": "Step 2: Add Soil Test Details", "info_soil_analysis": "Visual Analysis: Your soil looks like **{soil_type}** with **{organic_matter}** organic matter.",
        "button_get_plan": "Get My Crop Action Plan", "success_crop": "Success! The best crop for you is: **{crop}**", "subheader_plan": "Your Action Plan for {crop}", "button_start_over": "Start Over",
        "header_health": "AI Field Doctor: Diagnose Diseases, Pests & Weeds", "uploader_health": "Upload a photo of a sick leaf, an unknown pest, or a weed...", "button_diagnose": "Diagnose Now",
        "diagnosis_result": "AI Diagnosis Result", "threat_name": "Identified Threat", "threat_type": "Threat Type", "threat_action": "Recommended Action",
        "header_profit": "Profitability & Yield Forecaster", "subheader_profit": "Estimate potential earnings for your recommended crop.", "button_forecast": "Calculate Forecast for {crop}",
        "metric_yield": "Expected Yield", "metric_price": "Live Market Price", "metric_revenue": "Estimated Revenue", "warning_no_crop": "Please get a crop recommendation first.",
        "header_harvest": "AI Harvest & Market Advisor", "subheader_harvest": "Get the optimal time to harvest and sell for maximum profit.",
        "input_sowing_date": "Enter Your Crop Sowing Date:", "button_get_harvest_advice": "Get Harvest & Selling Advice", "harvest_date_est": "Estimated Harvest Date",
        "weather_outlook": "7-Day Weather Outlook", "market_trend": "APMC Market Trend", "final_advice": "Your AI-Powered Strategic Advice",
        "header_water": "AI Water Advisor", "subheader_water": "Get a daily irrigation schedule to save water.", "button_water_advice": "Get Today's Watering Advice",
        "subheader_weather_sim": "Today's Weather (Simulated for Bangarapet)", "subheader_advice": "Your Personalized Recommendation", "warning_no_soil": "Please complete the soil analysis first.",
        "header_wellness": "Proactive Tips for Healthy Plants", "wellness_intro": "Preventing diseases is better than curing them.", "wellness_soil_header": "1. Healthy Soil", "wellness_water_header": "2. Smart Watering", "wellness_pest_header": "3. Pest Management",
        "header_sms_demo": "SMS / Voice (IVR) Service Simulation", "subheader_sms_demo": "This shows how a farmer with a basic phone can get advice.", "phone_input_label": "Enter Farmer's 10-digit Phone Number:", "button_send_sms": "Simulate Sending SMS Recommendation"
    },
    'kn': {
        "title": "ಸ್ಮಾರ್ಟ್ ಆಗ್ರೋ AI", "welcome": "ಸ್ವಾಗತ! ಉತ್ತಮ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ನಮ್ಮ AI ಬಳಸಿ.",
        "tab_crop": "🌾 ಬೆಳೆ ಯೋಜನೆ", "tab_health": "🔬 ಫೀಲ್ಡ್ ಡಾಕ್ಟರ್", "tab_profit": "💰 ಲಾಭದ ಮುನ್ಸೂಚನೆ", "tab_harvest": "📈 ಕೊಯ್ಲು ಸಲಹೆಗಾರ", "tab_water": "💧 ನೀರಿನ ಸಲಹೆಗಾರ", "tab_wellness": "💚 ಆರೋಗ್ಯ ಸಲಹೆಗಳು", "tab_sms": "📱 SMS ಪ್ರಾತ್ಯಕ್ಷಿಕೆ",
        "header_harvest": "AI ಕೊಯ್ಲು ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಸಲಹೆಗಾರ", "subheader_harvest": "ಗರಿಷ್ಠ ಲಾಭಕ್ಕಾಗಿ ಕೊಯ್ಲು ಮತ್ತು ಮಾರಾಟ ಮಾಡಲು ಉತ್ತಮ ಸಮಯವನ್ನು ಪಡೆಯಿರಿ.",
        "input_sowing_date": "ನಿಮ್ಮ ಬೆಳೆ ಬಿತ್ತನೆ ದಿನಾಂಕವನ್ನು ನಮೂದಿಸಿ:", "button_get_harvest_advice": "ಕೊಯ್ಲು ಮತ್ತು ಮಾರಾಟ ಸಲಹೆ ಪಡೆಯಿರಿ", "harvest_date_est": "ಅಂದಾಜು ಕೊಯ್ಲು ದಿನಾಂಕ",
        "weather_outlook": "7-ದಿನಗಳ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ", "market_trend": "APMC ಮಾರುಕಟ್ಟೆ ಪ್ರವೃತ್ತಿ", "final_advice": "ನಿಮ್ಮ AI-ಚಾಲಿತ ತಂತ್ರಜ್ಞಾನ ಸಲಹೆ",
        "role_selector_title": "ನಿಮ್ಮ ಪಾತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "role_farmer": "ನಾನು ರೈತ", "role_kiosk": "ನಾನು ಕಿಯೋಸ್ಕ್ ಆಪರೇಟರ್", "kiosk_info": "ಈ ಮೋಡ್ ಅನೇಕ ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡಲು ನಿಮಗೆ ಅನುವು ಮಾಡಿಕೊಡುತ್ತದೆ.",
        "header_crop": "ನಿಮ್ಮ ಸಂಪೂರ್ಣ ಬೆಳೆ ಕ್ರಿಯಾ ಯೋಜನೆ ಪಡೆಯಿರಿ", "button_get_plan": "ನನ್ನ ಬೆಳೆ ಕ್ರಿಯಾ ಯೋಜನೆ ಪಡೆಯಿರಿ", "success_crop": "ಯಶಸ್ಸು! ನಿಮಗಾಗಿ ಉತ್ತಮ ಬೆಳೆ: **{crop}**"
        # ... other Kannada translations
    },
    'hi': {
        "title": "स्मार्ट एग्रो AI", "welcome": "आपका स्वागत है! बेहतर निर्णयों के लिए हमारे AI का उपयोग करें।",
        "tab_crop": "🌾 फसल योजना", "tab_health": "🔬 फील्ड डॉक्टर", "tab_profit": "💰 लाभ पूर्वानुमान", "tab_harvest": "📈 कटाई सलाहकार", "tab_water": "💧 जल सलाहकार", "tab_wellness": "💚 स्वास्थ्य सुझाव", "tab_sms": "📱 SMS डेमो",
        "header_harvest": "एआई कटाई और बाजार सलाहकार", "subheader_harvest": "अधिकतम लाभ के लिए कटाई और बेचने का इष्टतम समय प्राप्त करें।",
        "input_sowing_date": "अपनी फसल बुवाई की तारीख दर्ज करें:", "button_get_harvest_advice": "कटाई और बिक्री की सलाह प्राप्त करें", "harvest_date_est": "अनुमानित कटाई तिथि",
        "weather_outlook": "7-दिन का मौसम पूर्वानुमान", "market_trend": "एपीएमसी बाजार की प्रवृत्ति", "final_advice": "आपकी एआई-संचालित रणनीतिक सलाह",
        "role_selector_title": "अपनी भूमिका चुनें", "role_farmer": "मैं एक किसान हूँ", "role_kiosk": "मैं एक कियोस्क ऑपरेटर हूँ", "kiosk_info": "यह मोड आपको कई किसानों की सहायता करने में मदद करता है।",
        "header_crop": "अपनी पूरी फसल कार्य योजना प्राप्त करें", "button_get_plan": "मेरी फसल कार्य योजना प्राप्त करें", "success_crop": "सफलता! आपके लिए सबसे अच्छी फसल है: **{crop}**"
        # ... other Hindi translations
    }
}

# --- APP LAYOUT ---
st.sidebar.title("Language / ಭಾಷೆ / भाषा")
lang_display = st.sidebar.selectbox("Select language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[lang_display]
T = TEXT.get(lang_code, TEXT['en']) # Fallback to English

st.sidebar.title(T.get("role_selector_title", "Select Your Role"))
user_role = st.sidebar.radio("", (T.get("role_farmer", "I am a Farmer"), T.get("role_kiosk", "I am a Kiosk Operator")))
if T.get("role_kiosk", "I am a Kiosk Operator") in user_role: st.sidebar.info(T.get("kiosk_info", "This mode helps you assist multiple farmers."))

# Initialize Session State
for key in ['soil_analysis_done', 'soil_analysis_result', 'crop_recommendation_result']:
    if key not in st.session_state: st.session_state[key] = None

st.title(T.get("title", "SmartAgro AI")); st.markdown(T.get("welcome", "Welcome!"))

# --- TABS (7 FEATURES) ---
tab_keys = ["tab_crop", "tab_health", "tab_profit", "tab_harvest", "tab_water", "tab_wellness", "tab_sms"]
tab_names = [T.get(key, key.replace('_', ' ').title()) for key in tab_keys]
tabs = st.tabs(tab_names)

# Tab 1: Crop Plan
with tabs[0]:
    st.header(T.get("header_crop", "Get Your Complete Crop Action Plan"))
    if not st.session_state.get('soil_analysis_done'):
        st.subheader(T.get("subheader_crop_step1", "Step 1: Upload Soil Photo"))
        soil_image = st.file_uploader(T.get("uploader_soil", "Take a picture..."), type=["jpg", "jpeg", "png"])
        if soil_image:
            st.image(soil_image, caption='Your Soil', width=300)
            if st.button(T.get("button_analyze_soil", "Analyze Soil Visually"), use_container_width=True):
                with st.spinner("..."):
                    files = {'file': (soil_image.name, soil_image.getvalue(), soil_image.type)}
                    try:
                        response = requests.post("http://127.0.0.1:5000/analyze_soil_image", files=files)
                        response.raise_for_status()
                        st.session_state.soil_analysis_result = response.json()
                        st.session_state.soil_analysis_done = True; st.rerun()
                    except requests.RequestException as e: st.error(f"Connection error: {e}")
    if st.session_state.get('soil_analysis_done'):
        st.subheader(T.get("subheader_crop_step2", "Step 2: Add Soil Test Details"))
        result = st.session_state.get('soil_analysis_result')
        if result and 'error' not in result: st.info(T.get("info_soil_analysis", "Visual Analysis: ...").format(soil_type=result['soil_type'], organic_matter=result['organic_matter_estimate']))
        col1, col2 = st.columns(2)
        with col1: n_val, p_val, k_val = st.number_input("N (kg/ha)", 0, 200, 90), st.number_input("P (kg/ha)", 0, 200, 42), st.number_input("K (kg/ha)", 0, 200, 43)
        with col2: ph_val, temp_val, humidity_val, rainfall_val = st.number_input("pH", 0.0, 14.0, 6.5, 0.1), st.number_input("Temp (°C)", -10.0, 60.0, 25.5, 0.1), st.number_input("Humidity (%)", 0.0, 100.0, 70.0, 0.1), st.number_input("Rainfall (mm)", 0.0, 500.0, 100.0, 0.1)
        if st.button(T.get("button_get_plan", "Get Plan"), use_container_width=True, type="primary"):
            payload = {'lang': lang_code, 'N': n_val, 'P': p_val, 'K': k_val, 'temperature': temp_val, 'humidity': humidity_val, 'ph': ph_val, 'rainfall': rainfall_val}
            with st.spinner("..."):
                try:
                    response = requests.post("http://127.0.0.1:5000/predict_crop", json=payload)
                    response.raise_for_status(); st.session_state.crop_recommendation_result = response.json()
                except requests.RequestException as e: st.error(f"Connection error: {e}")
    if st.session_state.get('crop_recommendation_result'):
        res = st.session_state.crop_recommendation_result
        st.success(T.get("success_crop", "Success! Best crop: {crop}").format(crop=res['recommended_crop'].title()))
        st.subheader(T.get("subheader_plan", "Your Action Plan for {crop}").format(crop=res['recommended_crop'].title()))
        if 'action_plan' in res:
            for step, details in res['action_plan'].items():
                with st.expander(f"**{step}**"):
                    for point in details: st.markdown(point)
    if st.session_state.get('soil_analysis_done'):
        if st.button(T.get("button_start_over", "Start Over")):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

# Tab 2: Field Doctor
with tabs[1]:
    st.header(T.get("header_health", "AI Field Doctor"))
    uploaded_file = st.file_uploader(T.get("uploader_health", "Upload a photo..."), type=["jpg", "jpeg", "png"], key="health_uploader")
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption='Image for Analysis', use_column_width=True)
        if st.button(T.get("button_diagnose", "Diagnose Now"), use_container_width=True, type="primary"):
            with st.spinner('...'):
                files, data = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}, {'lang': lang_code}
                try:
                    response = requests.post("http://127.0.0.1:5000/diagnose_threat", files=files, data=data)
                    response.raise_for_status(); result = response.json()
                    st.subheader(T.get("diagnosis_result", "AI Diagnosis Result")); col1, col2 = st.columns(2)
                    col1.metric(T.get("threat_name", "Threat"), result['threat_name']); col2.metric(T.get("threat_type", "Type"), result['threat_type'])
                    st.success(f"**{T.get('threat_action', 'Action')}:** {result['recommended_action']}")
                except requests.RequestException as e: st.error(f"Connection error: {e}")

# Tab 3: Profit Forecast
with tabs[2]:
    st.header(T.get("header_profit", "Profitability Forecaster"))
    if st.session_state.get('crop_recommendation_result'):
        crop = st.session_state.crop_recommendation_result['recommended_crop']
        st.info(f"Forecasting for your recommended crop: **{crop.title()}**")
        if st.button(T.get("button_forecast", "Calculate for {crop}").format(crop=crop.title()), use_container_width=True, type="primary"):
            with st.spinner("..."):
                try:
                    response = requests.post("http://127.0.0.1:5000/calculate_profitability", json={'crop': crop})
                    response.raise_for_status(); forecast = response.json()
                    col1, col2, col3 = st.columns(3)
                    col1.metric(T.get("metric_yield", "Yield"), forecast['yield_forecast']); col2.metric(T.get("metric_price", "Price"), forecast['market_price']); col3.metric(T.get("metric_revenue", "Revenue"), forecast['estimated_revenue'])
                except requests.RequestException as e: st.error(f"Connection error: {e}")
    else: st.warning(T.get("warning_no_crop", "Please get a crop recommendation first."))

# Tab 4: Harvest Advisor
with tabs[3]:
    st.header(T.get("header_harvest", "AI Harvest & Market Advisor"))
    st.markdown(T.get("subheader_harvest", "Get the optimal time to harvest and sell."))
    if st.session_state.get('crop_recommendation_result'):
        crop = st.session_state.crop_recommendation_result['recommended_crop']
        st.info(f"Creating a harvest plan for: **{crop.title()}**")
        sowing_date = st.date_input(T.get("input_sowing_date", "Sowing Date:"), value=date.today() - timedelta(days=60))
        if st.button(T.get("button_get_harvest_advice", "Get Harvest Advice"), use_container_width=True, type="primary"):
            with st.spinner("Analyzing market prices and weather forecasts..."):
                payload = {'crop': crop, 'sowing_date': str(sowing_date), 'lang': lang_code}
                try:
                    response = requests.post("http://127.0.0.1:5000/get_harvest_advice", json=payload)
                    response.raise_for_status(); result = response.json()
                    st.subheader("Your Harvest & Selling Plan")
                    col1, col2, col3 = st.columns(3)
                    col1.metric(T.get("harvest_date_est", "Est. Harvest"), result['harvest_date_estimate'])
                    col2.metric(T.get("weather_outlook", "Weather"), result['weather_outlook'])
                    col3.metric(T.get("market_trend", "Market"), result['market_trend'])
                    st.success(f"**{T.get('final_advice', 'Advice')}:** {result['advice']}")
                except requests.RequestException as e: st.error(f"Connection error: {e}")
    else: st.warning(T.get("warning_no_crop", "Please get a crop recommendation first."))

# Tab 5: Water Advisor
with tabs[4]:
    st.header(T.get("header_water", "AI Water Advisor"))
    if st.session_state.get('soil_analysis_result') and 'error' not in st.session_state.soil_analysis_result:
        soil_type = st.session_state.soil_analysis_result['soil_type']
        st.info(f"Using your analyzed soil type: **{soil_type}**")
        if st.button(T.get("button_water_advice", "Get Today's Advice"), use_container_width=True, type="primary"):
            with st.spinner("..."):
                try:
                    response = requests.post("http://127.0.0.1:5000/get_watering_advice", json={'soil_type': soil_type, 'lang': lang_code})
                    response.raise_for_status(); result = response.json()
                    weather, advice = result['weather'], result['advice']
                    st.subheader(T.get("subheader_weather_sim", "Today's Weather")); col1, col2, col3 = st.columns(3)
                    col1.metric("Temperature", f"{weather['temp']} °C"); col2.metric("Humidity", f"{weather['humidity']} %"); col3.metric("Forecast", weather['forecast'])
                    st.subheader(T.get("subheader_advice", "Recommendation")); st.success(f"**{advice}**")
                except requests.RequestException as e: st.error(f"Connection error: {e}")
    else: st.warning(T.get("warning_no_soil", "Please complete the soil analysis first."))

# Tab 6: Wellness Tips
with tabs[5]:
    st.header(T.get("header_wellness", "Wellness Tips")); st.markdown(T.get("wellness_intro", "Prevention is better than cure."))
    st.subheader(T.get("wellness_soil_header", "Soil")); st.markdown("- Add compost.\n- Rotate crops.\n- Avoid compaction.")
    st.subheader(T.get("wellness_water_header", "Watering")); st.markdown("- Water early.\n- Use drip irrigation.\n- Avoid overwatering.")
    st.subheader(T.get("wellness_pest_header", "Pests")); st.markdown("- Encourage predators.\n- Use neem oil.\n- Inspect regularly.")

# Tab 7: SMS Demo
with tabs[6]:
    st.header(T.get("header_sms_demo", "SMS Simulation")); st.markdown(T.get("subheader_sms_demo", "For basic phones."))
    phone = st.text_input(T.get("phone_input_label", "Phone Number:"), max_chars=10, value="9988776655")
    if st.button(T.get("button_send_sms", "Simulate SMS"), use_container_width=True):
        if phone and len(phone) == 10 and st.session_state.get('crop_recommendation_result'):
            with st.spinner("..."):
                crop = st.session_state.crop_recommendation_result['recommended_crop']
                try:
                    response = requests.post("http://127.0.0.1:5000/simulate_sms", json={'lang': lang_code, 'crop': crop, 'phone_number': phone})
                    response.raise_for_status(); sms_message = response.json()['sms_message']
                    st.success("✅ SMS Sent!"); st.info(sms_message)
                except requests.RequestException as e: st.error(f"Connection Error: {e}")
        else: st.warning("Please get a crop recommendation and enter a valid 10-digit number first.")


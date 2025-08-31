# streamlit_app.py
# SmartAgro AI – Unified, robust Streamlit app (runs with or without models)

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import joblib

# ---------------------------
# Page config (must be first)
# ---------------------------
st.set_page_config(page_title="SmartAgro AI", page_icon="🌱", layout="wide")

# ---------------------------
# Constants & Dictionaries
# ---------------------------
LANGUAGES = {"English": "en", "ಕನ್ನಡ": "kn", "हिंदी": "hi"}

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

        "header_water": "💧 AI Water Advisor",
        "subheader_water": "Get a hyper-personalized daily irrigation schedule to save water and maximize yield.",
        "button_water_advice": "Get Today's Watering Advice",
        "subheader_weather_sim": "Today's Weather (Simulated for Bangarapet)",
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

        "header_wellness": "Proactive Tips for Healthy Plants",
        "wellness_intro": "Preventing diseases is better than curing them. Here are some tips to keep your plants healthy.",
        "wellness_soil_header": "1. Healthy Soil",
        "wellness_soil_points": [
            "- Regularly add compost.",
            "- Practice crop rotation.",
            "- Avoid soil compaction."
        ],
        "wellness_water_header": "2. Smart Watering",
        "wellness_water_points": [
            "- Water early in the morning.",
            "- Use drip irrigation.",
            "- Avoid overwatering."
        ],
        "wellness_pest_header": "3. Pest Management",
        "wellness_pest_points": [
            "- Encourage natural predators.",
            "- Use neem oil as a first defense.",
            "- Inspect plants regularly."
        ],

        "header_sms_demo": "SMS / Voice (IVR) Service Simulation",
        "subheader_sms_demo": "This shows how a farmer with a basic phone could get advice.",
        "ivr_title": "Simulate Crop Recommendation via IVR/SMS",
        "phone_input_label": "Enter Farmer's 10-digit Phone Number:",
        "ivr_instructions": "Imagine the farmer entered these values using their phone's keypad:",
        "button_send_sms": "Simulate Sending SMS Recommendation",
        "sms_sent_success": "SMS Sent Successfully!",
        "sms_preview": "Farmer would receive this message:",
        "error_phone_number": "Please enter a valid 10-digit phone number."
    },
    "kn": {
        "title": "ಸ್ಮಾರ್ಟ್ ಆಗ್ರೋ AI – ನಿಮ್ಮ ಜಮೀನಿನ ಸ್ಮಾರ್ಟ್ ಸಹಾಯಕ",
        "welcome": "ಸ್ವಾಗತ! ಉತ್ತಮ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ನಮ್ಮ AI ಬಳಸಿ.",
        "tab_crop": "🌾 ಬೆಳೆ ಶಿಫಾರಸು",
        "tab_health_diagnosis": "🌿 ಕ್ಷೇತ್ರ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆ",
        "tab_profit": "💰 ಲಾಭದ ಮುನ್ಸೂಚನೆ",
        "tab_water": "💧 AI ನೀರು ಸಲಹೆಗಾರ",
        "tab_harvest": "📈 ಸುಗ್ಗಿ ಸಲಹೆಗಾರ",
        "tab_wellness": "💚 ಆರೋಗ್ಯ ಸಲಹೆಗಳು",
        "tab_sms": "📱 SMS/IVR ಪ್ರಾತ್ಯಕ್ಷಿಕೆ",

        "role_selector_title": "ನಿಮ್ಮ ಪಾತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "role_farmer": "ನಾನು ರೈತ",
        "role_kiosk": "ನಾನು ಕಿಯೋಸ್ಕ್ ಆಪರೇಟರ್",
        "kiosk_info": "ಈ ಮೋಡ್ ಅನೇಕ ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡಲು ನಿಮಗೆ ಅನುವು ಮಾಡಿಕೊಡುತ್ತದೆ.",

        "header_crop": "ಸೂಕ್ತವಾದ ಬೆಳೆಯನ್ನು ಹುಡುಕಿ ಮತ್ತು ಸಂಪೂರ್ಣ ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ ಪಡೆಯಿರಿ",
        "subheader_crop_step1": "ಹಂತ 1: ನಿಮ್ಮ ಮಣ್ಣಿನ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "uploader_soil": "ನಿಮ್ಮ ಜಮೀನಿನ ಮಣ್ಣಿನ ಚಿತ್ರವನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ...",
        "button_analyze_soil": "ಮಣ್ಣನ್ನು ದೃಷ್ಟಿ ಮೂಲಕ ವಿಶ್ಲೇಷಿಸಿ",
        "spinner_soil": "AI ದೃಷ್ಟಿ ತಪಾಸಣೆ ನಡೆಸುತ್ತಿದೆ...",

        "subheader_crop_step2": "ಹಂತ 2: ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯಿಂದ ವಿವರಗಳನ್ನು ಸೇರಿಸಿ",
        "info_soil_analysis": "ದೃಶ್ಯ ವಿಶ್ಲೇಷಣೆ: ನಿಮ್ಮ ಮಣ್ಣು **{soil_type}** ಹಾಗು **{organic_matter}** ಜೈವಿಕ ವಸ್ತು ಹೊಂದಿದೆ.",
        "button_get_plan": "ನನ್ನ ಬೆಳೆ ಕಾರ್ಯಯೋಜನೆ ಪಡೆಯಿರಿ",
        "spinner_plan": "AI ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಯೋಜನೆಯನ್ನು ಸಿದ್ಧಪಡಿಸುತ್ತಿದೆ...",
        "success_crop": "ಯಶಸ್ಸು! ನಿಮ್ಮಿಗೆ ಅತ್ಯುತ್ತಮ ಬೆಳೆ: **{crop}**",
        "subheader_plan": "{crop}ಗಾಗಿ ನಿಮ್ಮ ಕಾರ್ಯಯೋಜನೆ",
        "button_start_over": "ಮತ್ತೆ ಆರಂಭಿಸಿ",

        "header_health": "AI ಫೀಲ್ಡ್ ಡಾಕ್ಟರ್: ರೋಗ, ಕೀಟ ಮತ್ತು ಕಳೆ ಪತ್ತೆ",
        "uploader_health": "ಅನಾರೋಗ್ಯ ಎಲೆ/ಅಪರಿಚಿತ ಕೀಟ/ಕಳೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ...",
        "button_diagnose": "ಈಗ ಪತ್ತೆಮಾಡಿ",
        "diagnosis_result": "AI ಪತ್ತೆ ಫಲಿತಾಂಶ",
        "threat_name": "ಗುರುತಿಸಿದ ಬೆದರಿಕೆ",
        "threat_type": "ಪರಿಭಾಷೆ",
        "threat_action": "ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ",

        "header_profit": "ಲಾಭ ಮತ್ತು ಉತ್ಪಾದನಾ ಪೂರ್ವಾನುಮಾನ",
        "subheader_profit": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ ಆಧಾರದಲ್ಲಿ ಆದಾಯ ಅಂದಾಜು ಪಡೆಯಿರಿ.",
        "button_forecast": "{crop}ಗಾಗಿ ಲೆಕ್ಕ ಹಾಕಿ",
        "subheader_results": "ಫಲಿತಾಂಶಗಳು",
        "metric_yield": "ಅಪೇಕ್ಷಿತ ಉತ್ಪಾದನೆ",
        "metric_price": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "metric_revenue": "ಅಂದಾಜು ಆದಾಯ",
        "warning_no_crop": "ದಯವಿಟ್ಟು ಮೊದಲು ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ.",

        "header_water": "💧 AI ನೀರು ಸಲಹೆಗಾರ",
        "subheader_water": "ದಿನಂಪ್ರತಿ ನೀರಾವರಿ ಸಲಹೆ – ನೀರನ್ನು ಉಳಿಸಿ, ಇಳುವರಿ ಹೆಚ್ಚಿಸಿ.",
        "button_water_advice": "ಇಂದಿನ ನೀರಾವರಿ ಸಲಹೆ",
        "subheader_weather_sim": "ಇಂದಿನ ಹವಾಮಾನ (ಸಿಮ್ಯುಲೇಷನ್)",
        "subheader_advice": "ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಸಲಹೆ",
        "warning_no_soil": "ಮೊದಲು ಮಣ್ಣಿನ ದೃಷ್ಟಿ ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣಗೊಳಿಸಿ.",

        "header_harvest": "📈 ಸುಗ್ಗಿ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಸಲಹೆ",
        "subheader_harvest": "ಅತ್ಯುತ್ತಮ ಕೊಯ್ಲು ಸಮಯ ಮತ್ತು ಮಾರಾಟ ತಂತ್ರ.",
        "sowing_date_label": "ಬಿತ್ತಿದ ದಿನಾಂಕ:",
        "button_harvest_advice": "ಕೊಯ್ಲು/ಮಾರಾಟ ಸಲಹೆ",
        "harvest_window_header": "ಉತ್ತಮ ಕೊಯ್ಲು ಕಿಟಕಿ",
        "market_outlook_header": "ಮಾರುಕಟ್ಟೆ ದೃಷ್ಟಿಕೋನ (ಸಿಮ್ಯುಲೇಟೆಡ್)",
        "weather_outlook_header": "ಹವಾಮಾನ (ಮುಂದಿನ 7 ದಿನ)",
        "final_advice_header": "ಅಂತಿಮ ಸಲಹೆ",

        "header_wellness": "ಆರೋಗ್ಯಕರ ಸಾಸ್ಯಗಳಿಗಾಗಿ ಸಲಹೆಗಳು",
        "wellness_intro": "ತಡೆಗಟ್ಟುವಿಕೆ ಚಿಕಿತ್ಸೆಗಿಂತ ಉತ್ತಮ.",
        "wellness_soil_header": "1. ಆರೋಗ್ಯಕರ ಮಣ್ಣು",
        "wellness_soil_points": [
            "- ನಿಯಮಿತವಾಗಿ ಕಂಪೋಸ್ಟ್ ಸೇರಿಸಿ.",
            "- ಬೆಳೆ ಪರಿವರ್ತನೆ ಅನುಸರಿಸಿ.",
            "- ಮಣ್ಣಿನ ಗಟ್ಟಿತನ ತಪ್ಪಿಸಿ."
        ],
        "wellness_water_header": "2. ಚತುರ ನೀರಾವರಿ",
        "wellness_water_points": [
            "- ಬೆಳಗ್ಗೆ ನೀರುಣಿಸಿ.",
            "- ಡ್ರಿಪ್ ನೀರಾವರಿ ಬಳಸಿ.",
            "- ಅತಿನೀರಾವರಿ ತಪ್ಪಿಸಿ."
        ],
        "wellness_pest_header": "3. ಕೀಟ ನಿರ್ವಹಣೆ",
        "wellness_pest_points": [
            "- ನೈಸರ್ಗಿಕ ಭಕ್ಷಕಗಳನ್ನು ಉತ್ತೇಜಿಸಿ.",
            "- ಮೊದಲ ರಕ್ಷಣೆಗೆ ಬೇವಿನ ಎಣ್ಣೆ ಬಳಸಿ.",
            "- ಸಸಿಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
        ],

        "header_sms_demo": "SMS / IVR ಸೇವೆ ಅನುಕರಣ",
        "subheader_sms_demo": "ಸಾಮಾನ್ಯ ಫೋನ್ ಇರುವ ರೈತರಿಗೆ ಹೇಗೆ ಸಲಹೆ ತಲುಪುತ್ತದೆ ಎಂಬುದು.",
        "ivr_title": "IVR/SMS ಮೂಲಕ ಬೆಳೆ ಶಿಫಾರಸು ಅನುಕರಣ",
        "phone_input_label": "ರೈತನ 10 ಅಂಕಿ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ:",
        "ivr_instructions": "ರೈತನು ಫೋನ್ ಕೀಪ್ಯಾಡ್ ಮೂಲಕ ಈ ಮೌಲ್ಯಗಳನ್ನು ನಮೂದಿಸಿದಂತೆ ಕಲ್ಪಿಸಿ:",
        "button_send_sms": "SMS ಶಿಫಾರಸು ಕಳುಹಿಸಿ",
        "sms_sent_success": "SMS ಯಶಸ್ವಿಯಾಗಿ ಕಳುಹಿಸಲಾಗಿದೆ!",
        "sms_preview": "ರೈತನಿಗೆ ಸಿಗುವ ಸಂದೇಶ:",
        "error_phone_number": "ದಯವಿಟ್ಟು ಸರಿಯಾದ 10 ಅಂಕಿ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ."
    },
    "hi": {
        "title": "स्मार्ट एग्रो AI – आपके खेत का स्मार्ट सहायक",
        "welcome": "आपका स्वागत है! बेहतर निर्णयों के लिए हमारे AI उपकरणों का उपयोग करें।",
        "tab_crop": "🌾 फसल सिफारिश",
        "tab_health_diagnosis": "🌿 क्षेत्र स्वास्थ्य निदान",
        "tab_profit": "💰 लाभ का पूर्वानुमान",
        "tab_water": "💧 AI जल सलाहकार",
        "tab_harvest": "📈 कटाई सलाहकार",
        "tab_wellness": "💚 स्वास्थ्य सुझाव",
        "tab_sms": "📱 SMS/IVR डेमो",

        "role_selector_title": "अपनी भूमिका चुनें",
        "role_farmer": "मैं एक किसान हूँ",
        "role_kiosk": "मैं एक कियोस्क ऑपरेटर हूँ",
        "kiosk_info": "यह मोड आपको कई किसानों की सहायता करने में मदद करता है।",

        "header_crop": "सही फसल चुनें और पूरी खेती गाइड पाएं",
        "subheader_crop_step1": "चरण 1: अपनी मिट्टी की फोटो अपलोड करें",
        "uploader_soil": "अपने खेत की मिट्टी की तस्वीर लें...",
        "button_analyze_soil": "दृश्य रूप से मिट्टी का विश्लेषण करें",
        "spinner_soil": "AI दृश्य जाँच कर रहा है...",

        "subheader_crop_step2": "चरण 2: मिट्टी परीक्षण के विवरण जोड़ें",
        "info_soil_analysis": "दृश्य विश्लेषण: आपकी मिट्टी **{soil_type}** है और **{organic_matter}** जैविक पदार्थ है.",
        "button_get_plan": "मेरा फसल प्लान प्राप्त करें",
        "spinner_plan": "AI आपका व्यक्तिगत प्लान बना रहा है...",
        "success_crop": "सफलता! आपके लिए सबसे अच्छी फसल: **{crop}**",
        "subheader_plan": "{crop} के लिए आपका एक्शन प्लान",
        "button_start_over": "दोबारा शुरू करें",

        "header_health": "AI फील्ड डॉक्टर: रोग, कीट और खरपतवार पहचान",
        "uploader_health": "बीमार पत्ती/अज्ञात कीट/खरपतवार की फोटो अपलोड करें...",
        "button_diagnose": "अब निदान करें",
        "diagnosis_result": "AI निदान परिणाम",
        "threat_name": "पहचाना गया खतरा",
        "threat_type": "खतरे का प्रकार",
        "threat_action": "सुझाई गई कार्रवाई",

        "header_profit": "लाभ और उपज पूर्वानुमान",
        "subheader_profit": "अनुशंसित फसल के आधार पर आय का अनुमान प्राप्त करें।",
        "button_forecast": "{crop} के लिए गणना करें",
        "subheader_results": "परिणाम",
        "metric_yield": "अपेक्षित उपज",
        "metric_price": "बाज़ार मूल्य",
        "metric_revenue": "अनुमानित राजस्व",
        "warning_no_crop": "कृपया पहले फसल सिफारिश प्राप्त करें.",

        "header_water": "💧 AI जल सलाहकार",
        "subheader_water": "दैनिक सिंचाई सलाह – पानी बचाएँ, उपज बढ़ाएँ।",
        "button_water_advice": "आज की सिंचाई सलाह",
        "subheader_weather_sim": "आज का मौसम (सिमुलेटेड)",
        "subheader_advice": "आपकी व्यक्तिगत सिफारिश",
        "warning_no_soil": "पहले दृश्य मिट्टी विश्लेषण पूरा करें.",

        "header_harvest": "📈 AI कटाई व बाजार सलाह",
        "subheader_harvest": "कटाई और बिक्री के लिए सर्वश्रेष्ठ समय।",
        "sowing_date_label": "बुवाई की तारीख:",
        "button_harvest_advice": "कटाई/बिक्री सलाह",
        "harvest_window_header": "उत्तम कटाई विंडो",
        "market_outlook_header": "बाजार दृष्टिकोण (सिम्युलेटेड)",
        "weather_outlook_header": "मौसम (अगले 7 दिन)",
        "final_advice_header": "अंतिम सिफारिश",

        "header_wellness": "स्वस्थ पौधों के लिए सुझाव",
        "wellness_intro": "रोकथाम इलाज से बेहतर है.",
        "wellness_soil_header": "1. स्वस्थ मिट्टी",
        "wellness_soil_points": [
            "- नियमित रूप से कम्पोस्ट डालें.",
            "- फसल चक्र अपनाएँ.",
            "- मिट्टी को सख्त होने से बचाएँ."
        ],
        "wellness_water_header": "2. स्मार्ट सिंचाई",
        "wellness_water_points": [
            "- सुबह के समय पानी दें.",
            "- ड्रिप सिंचाई का उपयोग करें.",
            "- अधिक पानी देने से बचें."
        ],
        "wellness_pest_header": "3. कीट प्रबंधन",
        "wellness_pest_points": [
            "- प्राकृतिक शिकारियों को बढ़ावा दें.",
            "- पहली रक्षा के रूप में नीम का तेल.",
            "- नियमित निरीक्षण करें."
        ],

        "header_sms_demo": "SMS/IVR सेवा सिमुलेशन",
        "subheader_sms_demo": "कैसे एक साधारण फोन वाला किसान सलाह पा सकता है.",
        "ivr_title": "IVR/SMS से फसल सिफारिश सिमुलेट करें",
        "phone_input_label": "किसान का 10-अंकों का फोन नंबर:",
        "ivr_instructions": "मान लें किसान ने ये मान दर्ज किए:",
        "button_send_sms": "SMS सिफारिश भेजें",
        "sms_sent_success": "SMS सफलतापूर्वक भेजा गया!",
        "sms_preview": "किसान को यह संदेश मिलेगा:",
        "error_phone_number": "कृपया मान्य 10-अंकों का नंबर दर्ज करें."
    },
}

CROP_ACTION_PLANS = {
    "en": {
        "rice": {
            "🌾 Land Preparation": [
                "- Plow the land 2-3 times and level it.",
                "- Ensure good drainage and a fine tilth."
            ],
            "🌱 Seed & Sowing": [
                "- Use high-yield, disease-resistant varieties.",
                "- Seed rate: 20-25 kg/acre.",
                "- Transplant seedlings after 25-30 days."
            ],
            "💧 Irrigation": [
                "- Maintain a water level of 2-5 cm.",
                "- Stop irrigation 15 days before harvesting."
            ],
            "🐞 Pest Control": [
                "- Monitor for stem borer and leaf folder.",
                "- Apply neem oil as a preventive measure."
            ],
        },
        "maize": {
            "🌾 Land Preparation": [
                "- Deep plow the land followed by harrowing.",
                "- The soil should be fine and weed-free."
            ],
            "🌱 Seed & Sowing": [
                "- Use a hybrid variety like HQPM-1.",
                "- Seed rate: 8-10 kg/acre.",
                "- Spacing: 60 cm (rows), 20 cm (plants)."
            ],
            "💧 Irrigation": [
                "- Critical stages: knee-high, flowering, grain filling."
            ],
            "🐞 Pest Control": [
                "- Watch for fall armyworm. Use pheromone traps."
            ],
        },
    },
    "kn": {"rice": {}, "maize": {}},
    "hi": {"rice": {}, "maize": {}},
}

CROP_DATA = {
    "rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050, "maturity_days": 120},
    "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100, "maturity_days": 100},
    "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500, "maturity_days": 150},
    "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000, "maturity_days": 365},
}

THREAT_DATABASE = {
    "en": {
        "fall_armyworm": {"type": "Pest", "solution": "Use pheromone traps. Severe: Emamectin Benzoate 5% SG."},
        "leaf_blight": {"type": "Disease", "solution": "Remove infected leaves; copper-based fungicide (e.g., Mancozeb)."},
        "amaranthus_viridis": {"type": "Weed", "solution": "Manual removal before flowering; targeted post-emergence herbicide."},
    },
    "kn": {
        "fall_armyworm": {"type": "ಕೀಟ", "solution": "ಫೆರೋಮೋನ್ ಬಲೆ. ತೀವ್ರತೆ: ಎಮಾಮೆಕ್ಟಿನ್ ಬೆನ್ಜೋಯೇಟ್ 5% SG."},
        "leaf_blight": {"type": "ರೋಗ", "solution": "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ; ತಾಮ್ರ ಆಧಾರಿತ ಶಿಲೀಂಧ್ರನಾಶಕ."},
        "amaranthus_viridis": {"type": "ಕಳೆ", "solution": "ಹೂಬಿಡುವ ಮೊದಲು ಕೈಯಿಂದ ತೆಗೆದುಹಾಕಿ; ಗುರಿತ ಕಳೆನಾಶಕ."},
    },
    "hi": {
        "fall_armyworm": {"type": "कीट", "solution": "फेरोमोन ट्रैप; गंभीर स्थिति: इमामेक्टिन बेंजोएट 5% SG."},
        "leaf_blight": {"type": "रोग", "solution": "संक्रमित पत्तियाँ हटाएँ; तांबा-आधारित कवकनाशी (जैसे मैंकोजेब)."},
        "amaranthus_viridis": {"type": "खरपतवार", "solution": "फूल आने से पहले हाथ से निकालें; लक्षित खरपतवारनाशी."},
    },
}

# ---------------------------
# Model Loading (robust)
# ---------------------------

class DummyCropModel:
    """Simple rule-based fallback if crop_model.pkl is missing."""
    def predict(self, X):
        preds = []
        for n, p, k, temp, hum, ph, rain in X:
            if ph < 6.3: preds.append("rice")
            elif temp >= 26 and hum >= 65: preds.append("maize")
            else: preds.append(random.choice(["rice", "maize"]))
        return preds

@st.cache_resource
def load_crop_model():
    # Try repo root then models/
    root = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
    candidates = [
        os.path.join(root, "crop_model.pkl"),
        os.path.join(root, "models", "crop_model.pkl"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception as e:
                st.error(f"⚠️ Could not load crop_model.pkl → {e}")
                break
    st.warning("⚠️ crop_model.pkl not found in repo root or models/. Using fallback dummy model.")
    return DummyCropModel()

@st.cache_resource
def load_field_doctor_model():
    """Optional TensorFlow model for image diagnosis."""
    root = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
    tf_path = os.path.join(root, "field_diagnosis_model.h5")
    if os.path.exists(tf_path):
        try:
            import tensorflow as tf  # heavy import only if model exists
            model = tf.keras.models.load_model(tf_path)
            return ("tf", model)
        except Exception as e:
            st.error(f"⚠️ Failed to load field_diagnosis_model.h5 → {e}")
    # fallback: rule/random
    return ("stub", None)

CROP_MODEL = load_crop_model()
FD_KIND, FD_MODEL = load_field_doctor_model()

# ---------------------------
# AI Logic
# ---------------------------

def analyze_soil_image(image_file):
    with Image.open(image_file) as img:
        avg_color = np.array(img.convert("RGB")).mean(axis=(0, 1))
        brightness = float(np.mean(avg_color))
        if brightness < 80:
            return {"soil_type": "Clay Loam", "organic_matter_estimate": "High"}
        elif brightness < 140:
            return {"soil_type": "Loamy Soil", "organic_matter_estimate": "Moderate"}
        else:
            return {"soil_type": "Sandy Soil", "organic_matter_estimate": "Low"}

def predict_crop_and_plan(model, data, lang):
    # model always exists (dummy if needed)
    prediction_result = model.predict([data])[0]
    action_plan = CROP_ACTION_PLANS.get(lang, CROP_ACTION_PLANS["en"]).get(
        str(prediction_result).lower(), {}
    )
    n_diff, p_diff = 90 - data[0], 42 - data[1]
    rec_urea = 50 + (n_diff / 10) * 5
    rec_dap = 50 + (p_diff / 10) * 2.5

    fert_templates = {
        "en": f"- Nitrogen is **{'low' if n_diff > 0 else 'high'}**. Apply **{rec_urea:.1f} kg Urea**.",
        "kn": f"- ಸಾರಜನಕ **{'ಕಡಿಮೆ' if n_diff > 0 else 'ಹೆಚ್ಚು'}**. **{rec_urea:.1f} ಕೆಜಿ ಯೂರಿಯಾ** ಬಳಸಿ.",
        "hi": f"- नाइट्रोजन **{'कम' if n_diff > 0 else 'अधिक'}** है। **{rec_urea:.1f} किग्रा यूरिया** डालें.",
    }
    action_plan = dict(action_plan)  # copy to avoid mutating constants
    action_plan["🌿 Personalized Fertilizer Plan"] = [
        fert_templates.get(lang, fert_templates["en"]),
        f"- Phosphorus balance tip: target DAP ~ {rec_dap:.1f} kg.",
    ]
    return {"recommended_crop": str(prediction_result), "action_plan": action_plan}

def diagnose_threat(uploaded, lang):
    lang_db = THREAT_DATABASE.get(lang, THREAT_DATABASE["en"])
    if FD_KIND == "tf" and FD_MODEL is not None:
        # Minimal preproc example; adjust to your model's spec if needed
        import tensorflow as tf
        img = Image.open(uploaded).convert("RGB").resize((224, 224))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)
        preds = FD_MODEL.predict(arr)
        # Map first 3 classes to our keys (adjust label mapping to your model)
        classes = ["fall_armyworm", "leaf_blight", "amaranthus_viridis"]
        idx = int(np.argmax(preds[0])) if preds is not None else 0
        key = classes[idx % len(classes)]
    else:
        key = random.choice(["fall_armyworm", "leaf_blight", "amaranthus_viridis"])

    info = lang_db.get(key, {"type": "Unknown", "solution": "No solution found."})
    return {
        "threat_name": key.replace("_", " ").title(),
        "threat_type": info["type"],
        "recommended_action": info["solution"],
    }

def get_watering_advice(soil_type, lang):
    weather = {
        "temp": round(random.uniform(24.0, 32.0), 1),
        "humidity": random.randint(55, 85),
        "forecast": random.choice(["Sunny", "Cloudy", "Light Haze", "Chance of Rain"]),
    }
    advice_key = "default"
    if "Rain" in weather["forecast"]:
        advice_key = "rain_expected"
    elif "Sandy" in soil_type and weather["temp"] > 28:
        advice_key = "sandy_hot"
    elif "Clay" in soil_type and weather["temp"] < 26:
        advice_key = "clay_cool"
    elif weather["temp"] > 30:
        advice_key = "hot_day"

    templates = {
        "en": {
            "rain_expected": "NO watering needed. Rain is expected.",
            "sandy_hot": "HIGH watering needed (45-60 min).",
            "clay_cool": "LOW watering needed (15-20 min).",
            "hot_day": "MODERATE watering needed (30-40 min).",
            "default": "NORMAL watering needed (25-30 min).",
        },
        "kn": {
            "rain_expected": "ನೀರುಣಿಸುವ ಅಗತ್ಯವಿಲ್ಲ. ಮಳೆ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ.",
            "sandy_hot": "ಹೆಚ್ಚು ನೀರುಣಿಸುವ ಅಗತ್ಯ (45-60 ನಿಮಿಷ).",
            "clay_cool": "ಕಡಿಮೆ ನೀರುಣಿಸುವ ಅಗತ್ಯ (15-20 ನಿಮಿಷ).",
            "hot_day": "ಮಧ್ಯಮ ನೀರುಣಿಸುವ ಅಗತ್ಯ (30-40 ನಿಮಿಷ).",
            "default": "ಸಾಮಾನ್ಯ ನೀರುಣಿಸುವ ಅಗತ್ಯ (25-30 ನಿಮಿಷ).",
        },
        "hi": {
            "rain_expected": "पानी देने की आवश्यकता नहीं। बारिश की उम्मीद है।",
            "sandy_hot": "ज्यादा पानी दें (45-60 मिनट)।",
            "clay_cool": "कम पानी दें (15-20 मिनट)।",
            "hot_day": "मध्यम पानी दें (30-40 मिनट)।",
            "default": "सामान्य पानी दें (25-30 मिनट)।",
        },
    }
    return {"weather": weather, "advice": templates.get(lang, templates["en"]).get(advice_key)}

def get_harvest_advice(crop_name, sowing_date, lang):
    days = CROP_DATA.get(str(crop_name).lower(), {}).get("maturity_days", 100)
    if isinstance(sowing_date, datetime):
        sdate = sowing_date
    else:
        # st.date_input returns a date (no time); convert safely
        sdate = datetime.combine(sowing_date, datetime.min.time())
    harvest_date = sdate + timedelta(days=days)
    weather_forecast = random.choice(
        ["Stable, sunny weather", "Risk of heavy rain in 5 days", "Clear skies, ideal conditions"]
    )
    market_trend = random.choice(
        ["Prices are stable", "Prices are trending up by 5-8%", "Prices are expected to dip slightly"]
    )
    advice_key = "default"
    if "rain" in weather_forecast.lower():
        advice_key = "harvest_now"
    elif "stable" in weather_forecast.lower() and "up" in market_trend.lower():
        advice_key = "wait"

    templates = {
        "en": {
            "harvest_now": "URGENT: Harvest within 3 days. Heavy rain is forecast, but current prices are high.",
            "wait": "STRATEGIC: Hold your harvest for 5-7 days. Weather is stable and market prices are projected to rise.",
            "default": "STANDARD: Your crop is ready. Harvest when convenient; weather & market are stable.",
        },
        "kn": {
            "harvest_now": "ತುರ್ತು: 3 ದಿನಗಳಲ್ಲಿ ಕೊಯ್ಲು ಮಾಡಿ. ಭಾರೀ ಮಳೆಯ ಮುನ್ಸೂಚನೆ ಇದೆ; ಈಗ ಬೆಲೆಗಳು ಉತ್ತಮ.",
            "wait": "ತಂತ್ರ: 5-7 ದಿನ ಹಿಡಿದುಕೊಳ್ಳಿ. ಹವಾಮಾನ ಸ್ಥಿರ, ಮಾರುಕಟ್ಟೆ ಏರಿಕೆ ನಿರೀಕ್ಷೆ.",
            "default": "ಪ್ರಮಾಣಿತ: ನಿಮ್ಮ ಬೆಳೆ ಸಿದ್ಧ. ನಿಮ್ಮ ಅನುಕೂಲಕ್ಕೆ ಕೊಯ್ಲು ಮಾಡಿ.",
        },
        "hi": {
            "harvest_now": "जरूरी: 3 दिनों में कटाई करें। भारी बारिश का अनुमान है; मौजूदा कीमतें अच्छी हैं।",
            "wait": "रणनीतिक: 5-7 दिन रोकें। मौसम स्थिर है और कीमतें बढ़ सकती हैं।",
            "default": "मानक: आपकी फसल तैयार है। सुविधा अनुसार कटाई करें; मौसम/बाज़ार स्थिर हैं।",
        },
    }
    return {
        "harvest_window": f"{harvest_date.strftime('%d %b')} to {(harvest_date + timedelta(days=10)).strftime('%d %b, %Y')}",
        "market_outlook": market_trend,
        "weather_outlook": weather_forecast,
        "advice": templates.get(lang, templates["en"]).get(advice_key),
    }

# ---------------------------
# UI – Sidebar (Language/Role)
# ---------------------------
st.sidebar.title("Language / ಭಾಷೆ / भाषा")
lang_display = st.sidebar.selectbox(" ", list(LANGUAGES.keys()), key="lang_select")
lang_code = LANGUAGES.get(lang_display, "en")
T = TEXT.get(lang_code, TEXT["en"])

st.sidebar.title(T.get("role_selector_title", "Select Your Role"))
user_role = st.sidebar.radio(
    " ", (T.get("role_farmer", "I am a Farmer"), T.get("role_kiosk", "I am a Kiosk Operator")),
    key="role_radio"
)
if T.get("role_kiosk", "I am a Kiosk Operator") in user_role:
    st.sidebar.info(T.get("kiosk_info", "This mode helps you assist multiple farmers."))

# ---------------------------
# Session state init
# ---------------------------
for key, default in [
    ("soil_analysis_done", False),
    ("soil_analysis_result", None),
    ("crop_recommendation_result", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------
# Main
# ---------------------------
st.title(T.get("title", "SmartAgro AI"))
st.markdown(T.get("welcome", "Welcome!"))

tab_keys = ["tab_crop", "tab_health_diagnosis", "tab_profit", "tab_water", "tab_harvest", "tab_wellness", "tab_sms"]
tabs = st.tabs([T.get(k, k.replace("_", " ").title()) for k in tab_keys])

# --- Tab 0: Crop Recommendation ---
with tabs[0]:
    st.header(T.get("header_crop", "Crop Recommendation"))

    if not st.session_state.soil_analysis_done:
        st.subheader(T.get("subheader_crop_step1", "Upload a Soil Photo"))
        soil_image = st.file_uploader(
            T.get("uploader_soil", "Upload soil image..."),
            type=["jpg", "jpeg", "png"],
            key="soil_uploader",
        )
        if soil_image:
            st.image(soil_image, caption="Your Soil", width=300)
            if st.button(T.get("button_analyze_soil", "Analyze Soil"), key="btn_analyze_soil"):
                with st.spinner(T.get("spinner_soil", "Analyzing...")):
                    st.session_state.soil_analysis_result = analyze_soil_image(soil_image)
                    st.session_state.soil_analysis_done = True
                    st.rerun()

    if st.session_state.soil_analysis_done:
        st.subheader(T.get("subheader_crop_step2", "Enter Soil Test Values"))
        result = st.session_state.soil_analysis_result or {}
        if "error" not in result:
            st.info(
                T.get("info_soil_analysis", "Soil: {soil_type}, OM: {organic_matter}").format(
                    soil_type=result.get("soil_type", "Loam"),
                    organic_matter=result.get("organic_matter_estimate", "Moderate"),
                )
            )

        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("Nitrogen (N)", 0, 200, 90, key="input_n")
            p = st.number_input("Phosphorus (P)", 0, 200, 42, key="input_p")
            k = st.number_input("Potassium (K)", 0, 200, 43, key="input_k")
        with col2:
            temp = st.number_input("Temperature (°C)", -10.0, 60.0, 25.5, 0.1, key="input_temp")
            hum = st.number_input("Humidity (%)", 0.0, 100.0, 70.0, 0.1, key="input_hum")
            ph = st.number_input("Soil pH", 0.0, 14.0, 6.5, 0.1, key="input_ph")
            rain = st.number_input("Rainfall (mm)", 0.0, 500.0, 100.0, 0.1, key="input_rain")

        if st.button(T.get("button_get_plan", "Get Plan"), key="btn_get_plan", use_container_width=True, type="primary"):
            with st.spinner(T.get("spinner_plan", "Computing plan...")):
                features = [n, p, k, temp, hum, ph, rain]
                st.session_state.crop_recommendation_result = predict_crop_and_plan(CROP_MODEL, features, lang_code)

        if st.session_state.crop_recommendation_result:
            res = st.session_state.crop_recommendation_result
            crop_name = str(res["recommended_crop"]).title()
            st.success(T.get("success_crop", "Best crop: {crop}").format(crop=crop_name))
            st.subheader(T.get("subheader_plan", "Your Plan for {crop}").format(crop=crop_name))
            if "action_plan" in res:
                for step, details in res["action_plan"].items():
                    with st.expander(f"{step}"):
                        for point in details:
                            st.markdown(point)

        if st.button(T.get("button_start_over", "Start Over"), key="btn_start_over"):
            st.session_state.soil_analysis_done = False
            st.session_state.soil_analysis_result = None
            st.session_state.crop_recommendation_result = None
            st.rerun()

# --- Tab 1: Field Health Diagnosis ---
with tabs[1]:
    st.header(T.get("header_health", "Field Diagnosis"))
    uploaded_file = st.file_uploader(
        T.get("uploader_health", "Upload field image..."),
        type=["jpg", "jpeg", "png"],
        key="health_uploader",
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Image for Analysis", use_column_width=True)
        if st.button(T.get("button_diagnose", "Diagnose"), key="btn_diagnose", use_container_width=True, type="primary"):
            with st.spinner("Analyzing..."):
                result = diagnose_threat(uploaded_file, lang_code)
                st.subheader(T.get("diagnosis_result", "Diagnosis"))
                c1, c2 = st.columns(2)
                c1.metric(T.get("threat_name", "Threat"), result["threat_name"])
                c2.metric(T.get("threat_type", "Type"), result["threat_type"])
                st.success(f"**{T.get('threat_action', 'Action')}:** {result['recommended_action']}")

# --- Tab 2: Profit Forecast ---
with tabs[2]:
    st.header(T.get("header_profit", "Profit Forecast"))
    st.markdown(T.get("subheader_profit", "Estimate earnings."))
    if st.session_state.crop_recommendation_result:
        crop = st.session_state.crop_recommendation_result["recommended_crop"]
        st.info(f"Forecasting for your recommended crop: **{str(crop).title()}**")
        if st.button(
            T.get("button_forecast", "Calculate Forecast").format(crop=str(crop).title()),
            key="btn_forecast", use_container_width=True, type="primary"
        ):
            with st.spinner("Analyzing market data..."):
                info = CROP_DATA.get(str(crop).lower())
                if info:
                    revenue = info["yield_per_acre"] * info["market_price_per_quintal"]
                    st.subheader(T.get("subheader_results", "Results"))
                    c1, c2, c3 = st.columns(3)
                    c1.metric(T.get("metric_yield", "Yield"), f"{info['yield_per_acre']} Quintals/Acre")
                    c2.metric(T.get("metric_price", "Price"), f"₹{info['market_price_per_quintal']:,}/Quintal")
                    c3.metric(T.get("metric_revenue", "Revenue"), f"₹{revenue:,.2f} / Acre")
    else:
        st.warning(T.get("warning_no_crop", "Get crop recommendation first."))

# --- Tab 3: Water Advisor ---
with tabs[3]:
    st.header(T.get("header_water", "Water Advisor"))
    st.markdown(T.get("subheader_water", "Daily irrigation schedule."))
    soil_ok = st.session_state.soil_analysis_result and "error" not in (st.session_state.soil_analysis_result or {})
    if soil_ok:
        soil_type = st.session_state.soil_analysis_result.get("soil_type", "Loamy Soil")
        st.info(f"Using your analyzed soil type: **{soil_type}**")
        if st.button(T.get("button_water_advice", "Get Watering Advice"), key="btn_water", use_container_width=True, type="primary"):
            with st.spinner("Checking conditions..."):
                result = get_watering_advice(soil_type, lang_code)
                weather, advice = result["weather"], result["advice"]
                st.subheader(T.get("subheader_weather_sim", "Today's Weather"))
                c1, c2, c3 = st.columns(3)
                c1.metric("Temperature", f"{weather['temp']} °C")
                c2.metric("Humidity", f"{weather['humidity']} %")
                c3.metric("Forecast", weather["forecast"])
                st.subheader(T.get("subheader_advice", "Advice"))
                st.success(f"**{advice}**")
    else:
        st.warning(T.get("warning_no_soil", "Complete soil analysis first."))

# --- Tab 4: Harvest Advisor ---
with tabs[4]:
    st.header(T.get("header_harvest", "Harvest Advisor"))
    st.markdown(T.get("subheader_harvest", "Best time to harvest & sell."))
    if st.session_state.crop_recommendation_result:
        crop = st.session_state.crop_recommendation_result["recommended_crop"]
        st.info(f"Get harvest advice for: **{str(crop).title()}**")
        sowing_date = st.date_input(T.get("sowing_date_label", "Sowing date"), datetime.now() - timedelta(days=60), key="sowing_date")
        if st.button(T.get("button_harvest_advice", "Harvest & Selling Advice"), key="btn_harvest", use_container_width=True, type="primary"):
            with st.spinner("Analyzing forecasts..."):
                result = get_harvest_advice(crop, sowing_date, lang_code)
                st.subheader(T.get("harvest_window_header", "Harvest Window"))
                st.info(result["harvest_window"])
                c1, c2 = st.columns(2)
                c1.subheader(T.get("market_outlook_header", "Market Outlook"))
                c1.write(result["market_outlook"])
                c2.subheader(T.get("weather_outlook_header", "Weather Outlook"))
                c2.write(result["weather_outlook"])
                st.subheader(T.get("final_advice_header", "Final Recommendation"))
                st.success(f"**{result['advice']}**")
    else:
        st.warning(T.get("warning_no_crop", "Get crop recommendation first."))

# --- Tab 5: Wellness Tips ---
with tabs[5]:
    st.header(T.get("header_wellness", "Wellness Tips"))
    st.markdown(T.get("wellness_intro", "Prevention is better than cure."))
    st.subheader(T.get("wellness_soil_header", "Healthy Soil"))
    for point in T.get("wellness_soil_points", []):
        st.markdown(point)
    st.subheader(T.get("wellness_water_header", "Smart Watering"))
    for point in T.get("wellness_water_points", []):
        st.markdown(point)
    st.subheader(T.get("wellness_pest_header", "Pest Management"))
    for point in T.get("wellness_pest_points", []):
        st.markdown(point)

# --- Tab 6: SMS/IVR Demo ---
with tabs[6]:
    st.header(T.get("header_sms_demo", "SMS / IVR Demo"))
    st.markdown(T.get("subheader_sms_demo", "How basic-phone users get advice."))
    st.subheader(T.get("ivr_title", "Simulate via IVR/SMS"))

    phone = st.text_input(T.get("phone_input_label", "Phone number"), "9988776655", max_chars=10, key="sms_phone")
    st.markdown(T.get("ivr_instructions", "Assume these values entered via keypad:"))

    col1, col2 = st.columns(2)
    with col1:
        n_sms = st.number_input("N", 0, 200, 100, key="sms_n")
        p_sms = st.number_input("P", 0, 200, 50, key="sms_p")
    with col2:
        k_sms = st.number_input("K", 0, 200, 50, key="sms_k")
        ph_sms = st.number_input("pH", 0.0, 14.0, 7.0, 0.1, key="sms_ph")

    if st.button(T.get("button_send_sms", "Send SMS"), key="btn_sms_send", use_container_width=True):
        if phone and len(str(phone)) == 10 and str(phone).isdigit():
            with st.spinner("Sending SMS..."):
                features = [n_sms, p_sms, k_sms, 26.0, 80.0, ph_sms, 120.0]
                result = predict_crop_and_plan(CROP_MODEL, features, lang_code)
                crop_name = str(result["recommended_crop"])
                templates = {
                    "en": f"SmartAgro AI for +91-{phone}: Best crop is **{crop_name}**. Visit your local kiosk for a full plan.",
                    "kn": f"+91-{phone}: ಉತ್ತಮ ಬೆಳೆ **{crop_name}**. ಪೂರ್ಣ ಯೋಜನೆಗಾಗಿ ಸ್ಥಳೀಯ ಕಿಯೋಸ್ಕ್ಗೆ ಭೇಟಿ ನೀಡಿ.",
                    "hi": f"+91-{phone}: सबसे अच्छी फसल **{crop_name}**। पूरी योजना के लिए अपने स्थानीय कियोस्क पर जाएँ.",
                }
                st.success(T.get("sms_sent_success", "SMS Sent Successfully!"))
                st.info(templates.get(lang_code, templates["en"]))
        else:
            st.error(T.get("error_phone_number", "Enter a valid 10-digit number."))

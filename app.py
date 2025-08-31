# app.py

from flask import Flask, request, jsonify
import joblib
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# --- KNOWLEDGE BASES (FULLY MULTILINGUAL) ---
CROP_ACTION_PLANS = {
    'en': {"rice": {"🌾 Land Preparation": ["Plow 2-3 times and level it."], "🌱 Seed & Sowing": ["Use high-yield varieties."], "💧 Irrigation": ["Maintain 2-5 cm water level."], "🐞 Pest Control": ["Monitor for stem borer."]}, "maize": {"🌾 Land Preparation": ["Deep plow the land."], "🌱 Seed & Sowing": ["Use a hybrid variety."], "💧 Irrigation": ["Water at critical stages."], "🐞 Pest Control": ["Watch for fall armyworm."]}},
    'kn': {"rice": {"🌾 ಭೂಮಿ ಸಿದ್ಧತೆ": ["ಭೂಮಿಯನ್ನು 2-3 ಬಾರಿ ಉಳುಮೆ ಮಾಡಿ."]}, "maize": {"🌾 ಭೂಮಿ ಸಿದ್ಧತೆ": ["ಆಳವಾಗಿ ಉಳುಮೆ ಮಾಡಿ."]}},
    'hi': {"rice": {"🌾 खेत की तैयारी": ["खेत को 2-3 बार जोतें।"]}, "maize": {"🌾 खेत की तैयारी": ["गहरी जुताई करें।"]}}
}
CROP_DATA = {"rice": {"yield_per_acre": 22, "market_price_per_quintal": 2050}, "maize": {"yield_per_acre": 25, "market_price_per_quintal": 2100}, "pigeonpeas": {"yield_per_acre": 8, "market_price_per_quintal": 6500}, "coffee": {"yield_per_acre": 4, "market_price_per_quintal": 15000}}
THREAT_DATABASE = {
    'en': {"fall_armyworm": {"type": "Pest", "solution": "Use pheromone traps."}, "leaf_blight": {"type": "Disease", "solution": "Apply a copper-based fungicide."}, "amaranthus_viridis": {"type": "Weed", "solution": "Manual removal is effective."}},
    'kn': {"fall_armyworm": {"type": "ಕೀಟ", "solution": "ಫೆರೋಮೋನ್ ಬಲೆಗಳನ್ನು ಬಳಸಿ."}, "leaf_blight": {"type": "ರೋಗ", "solution": "ತಾಮ್ರ ಆಧಾರಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ."}, "amaranthus_viridis": {"type": "ಕಳೆ", "solution": "ಕೈಯಿಂದ ತೆಗೆಯುವುದು ಪರಿಣಾಮಕಾರಿ."}},
    'hi': {"fall_armyworm": {"type": "कीट", "solution": "फेरोमोन ट्रैप का प्रयोग करें।"}, "leaf_blight": {"type": "रोग", "solution": "तांबा आधारित कवकनाशी का प्रयोग करें।"}, "amaranthus_viridis": {"type": "खरपतवार", "solution": "हाथ से निकालना प्रभावी है।"}}
}
CROP_MATURITY_DATA = {"rice": 120, "maize": 100, "pigeonpeas": 180, "coffee": 1500}

# --- SETUP ---
crop_model = joblib.load('models/crop_model.pkl')
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- API ENDPOINTS ---

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    data = request.get_json(force=True)
    lang = data.get('lang', 'en')
    features = [data['N'], data['P'], data['K'], data['temperature'], data['humidity'], data['ph'], data['rainfall']]
    prediction_result = crop_model.predict([features])[0]
    action_plan = CROP_ACTION_PLANS.get(lang, {}).get(prediction_result.lower(), {})
    n_diff = 90 - data['N']
    rec_urea = 50 + (n_diff / 10) * 5
    fert_advice_templates = {
        'en': f"- Your soil is {'low' if n_diff > 0 else 'high'} in Nitrogen. We recommend applying **{rec_urea:.1f} kg of Urea**.",
        'kn': f"- ನಿಮ್ಮ ಮಣ್ಣಿನಲ್ಲಿ ಸಾರಜನಕ {'ಕಡಿಮೆ' if n_diff > 0 else 'ಹೆಚ್ಚು'} ಇದೆ. ನಾವು **{rec_urea:.1f} ಕೆಜಿ ಯೂರಿಯಾ** ಬಳಸಲು ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ.",
        'hi': f"- आपकी मिट्टी में नाइट्रोजन {'कम' if n_diff > 0 else 'अधिक'} है। हम **{rec_urea:.1f} किलोग्राम यूरिया** डालने की सलाह देते हैं।"
    }
    action_plan["🌿 Personalized Fertilizer Plan"] = [fert_advice_templates[lang]]
    return jsonify({'recommended_crop': prediction_result, 'action_plan': action_plan})

@app.route('/analyze_soil_image', methods=['POST'])
def analyze_soil_image_endpoint():
    if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            with Image.open(filepath) as img:
                avg_color = np.array(img.convert('RGB')).mean(axis=(0, 1))
                brightness = sum(avg_color) / 3
                if brightness < 80: soil_type, organic_matter = "Clay Loam", "High"
                elif brightness < 140: soil_type, organic_matter = "Loamy Soil", "Moderate"
                else: soil_type, organic_matter = "Sandy Soil", "Low"
                return jsonify({"soil_type": soil_type, "organic_matter_estimate": organic_matter})
        except Exception as e: return jsonify({"error": str(e)})

@app.route('/diagnose_threat', methods=['POST'])
def diagnose_threat():
    if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    lang = request.form.get('lang', 'en')
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400
    if file:
        threats = ["fall_armyworm", "leaf_blight", "amaranthus_viridis"]
        identified_threat_key = random.choice(threats)
        threat_info = THREAT_DATABASE.get(lang, {}).get(identified_threat_key, {"type": "Unknown", "solution": "No solution found."})
        return jsonify({'threat_name': identified_threat_key.replace('_', ' ').title(), 'threat_type': threat_info['type'], 'recommended_action': threat_info['solution']})

@app.route('/calculate_profitability', methods=['POST'])
def calculate_profitability():
    data = request.get_json(force=True)
    crop_name = data.get('crop', '').lower()
    crop_info = CROP_DATA.get(crop_name)

    if not crop_info:
        return jsonify({'error': 'Data not found for this crop.'})
    
    y = crop_info['yield_per_acre']
    p = crop_info['market_price_per_quintal']
    
    return jsonify({
        'yield_forecast': f"{y} Q/Acre", 
        'market_price': f"₹{p:,}/Q", 
        'estimated_revenue': f"₹{y*p:,.2f}/Acre"
    })

@app.route('/get_watering_advice', methods=['POST'])
def get_watering_advice():
    data = request.get_json(force=True); soil_type, lang = data.get('soil_type', 'Loamy Soil'), data.get('lang', 'en')
    conditions, temp, humidity = ["Sunny", "Cloudy", "Light Haze", "Chance of Rain"], round(random.uniform(24.0, 32.0), 1), random.randint(55, 85)
    weather = {"temp": temp, "humidity": humidity, "forecast": random.choice(conditions)}
    advice_key = 'default'
    if "Rain" in weather['forecast']: advice_key = 'rain_expected'
    elif "Sandy" in soil_type and temp > 28: advice_key = 'sandy_hot'
    elif "Clay" in soil_type and temp < 26: advice_key = 'clay_cool'
    elif temp > 30: advice_key = 'hot_day'
    advice_templates = {
        'en': {'rain_expected': "NO watering needed. Rain is expected.", 'sandy_hot': "HIGH watering needed (45-60 mins).", 'clay_cool': "LOW watering needed (15-20 mins).", 'hot_day': "MODERATE watering needed (30-40 mins).", 'default': "NORMAL watering needed (25-30 mins)."},
        'kn': {'rain_expected': "ನೀರುಣಿಸುವ ಅಗತ್ಯವಿಲ್ಲ. ಮಳೆ ನಿರೀಕ್ಷಿತವಾಗಿದೆ.", 'sandy_hot': "ಹೆಚ್ಚು ನೀರುಣಿಸಿ (45-60 ನಿಮಿಷ).", 'clay_cool': "ಕಡಿಮೆ ನೀರುಣಿಸಿ (15-20 ನಿಮಿಷ).", 'hot_day': "ಮಧ್ಯಮ ನೀರುಣಿಸಿ (30-40 ನಿಮಿಷ).", 'default': "ಸಾಮಾನ್ಯ ನೀರುಣಿಸಿ (25-30 ನಿಮಿಷ)."},
        'hi': {'rain_expected': "पानी देने की आवश्यकता नहीं है। बारिश की उम्मीद है।", 'sandy_hot': "अधिक पानी दें (45-60 मिनट)।", 'clay_cool': "कम पानी दें (15-20 मिनट)।", 'hot_day': "मध्यम पानी दें (30-40 मिनट)।", 'default': "सामान्य पानी दें (25-30 मिनट)।"}
    }
    return jsonify({'weather': weather, 'advice': advice_templates[lang][advice_key]})

@app.route('/get_harvest_advice', methods=['POST'])
def get_harvest_advice():
    data = request.get_json(force=True); crop_name, sowing_date_str, lang = data.get('crop'), data.get('sowing_date'), data.get('lang', 'en')
    maturity_days = CROP_MATURITY_DATA.get(crop_name.lower())
    if not maturity_days: return jsonify({'error': 'Maturity data not found.'})
    sowing_date = datetime.strptime(sowing_date_str, '%Y-%m-%d'); harvest_date = sowing_date + timedelta(days=maturity_days)
    weather, market = random.choice(["Clear Skies", "Rain Forecast", "Stable"]), random.choice(["Trending Up", "Stable", "Trending Down"])
    advice_key = 'default'
    if "Rain" in weather: advice_key = 'urgent_harvest_rain'
    elif "Up" in market and "Clear" in weather: advice_key = 'hold_harvest_market_up'
    elif "Down" in market: advice_key = 'harvest_now_market_down'
    advice_templates = {
        'en': {'urgent_harvest_rain': "URGENT HARVEST. Harvest within 3 days.", 'hold_harvest_market_up': "HOLD HARVEST. Wait for 5-7 days.", 'harvest_now_market_down': "HARVEST NOW. Sell immediately.", 'default': "HARVEST SOON. Plan to harvest in 7-10 days."},
        'kn': {'urgent_harvest_rain': "ತುರ್ತು ಕೊಯ್ಲು. 3 ದಿನಗಳಲ್ಲಿ ಕೊಯ್ಲು ಮಾಡಿ.", 'hold_harvest_market_up': "ಕೊಯ್ಲು ತಡೆಹಿಡಿಯಿರಿ. 5-7 ದಿನ ಕಾಯಿರಿ.", 'harvest_now_market_down': "ಈಗಲೇ ಕೊಯ್ಲು ಮಾಡಿ. ತಕ್ಷಣ ಮಾರಾಟ ಮಾಡಿ.", 'default': "ಶೀಘ್ರದಲ್ಲೇ ಕೊಯ್ಲು ಮಾಡಿ."},
        'hi': {'urgent_harvest_rain': "तत्काल कटाई करें। 3 दिनों के भीतर कटाई करें।", 'hold_harvest_market_up': "कटाई रोकें। 5-7 दिन प्रतीक्षा करें।", 'harvest_now_market_down': "अभी कटाई करें। तुरंत बेचें।", 'default': "जल्द ही कटाई करें।"}
    }
    return jsonify({"harvest_date_estimate": harvest_date.strftime('%B %d, %Y'), "weather_outlook": weather, "market_trend": market, "advice": advice_templates[lang][advice_key]})

@app.route('/simulate_sms', methods=['POST'])
def simulate_sms():
    data = request.get_json(force=True); lang, crop, phone = data.get('lang', 'en'), data.get('crop', 'Unknown'), data.get('phone_number', 'farmer')
    sms_templates = {
        'en': f"SmartAgro AI Alert for +91-{phone}: Best crop is **{crop}**. Visit your local kiosk for a detailed plan.",
        'kn': f"+91-{phone} ಸಂಖ್ಯೆಗೆ ಸ್ಮಾರ್ಟ್ ಆಗ್ರೋ AI ಸಂದೇಶ: ಉತ್ತಮ ಬೆಳೆ **{crop}**. ವಿವರವಾದ ಯೋಜನೆಗಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.",
        'hi': f"+91-{phone} के लिए स्मार्ट एग्रो AI अलर्ट: सबसे अच्छी फसल **{crop}** है। विस्तृत योजना के लिए अपने स्थानीय कियोस्क पर जाएँ।"
    }
    return jsonify({'sms_message': sms_templates.get(lang, sms_templates['en'])})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


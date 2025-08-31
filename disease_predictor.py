# disease_predictor.py

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np

# Load a pre-trained model (MobileNetV2) for demonstration
# For a real application, you would fine-tune this on the PlantVillage dataset
model = MobileNetV2(weights='imagenet')

# For the demo, we'll map a predicted class to a disease name.
# In a real app, your model would be trained to output these classes directly.
# This is a simplified mapping for the demo.
CLASS_MAPPING = {
    'bell_pepper': 'Pepper Bell Bacterial Spot',
    'scab': 'Apple Scab',
    'black_rot': 'Apple Black Rot',
    'leaf_blight': 'Corn (Maize) Common Rust',
    'spot_disease': 'Tomato Leaf Spot',
    'strawberry': 'Strawberry Leaf Scorch'
}

def predict_disease(image_path):
    """
    Predicts the disease from an image file.
    NOTE: This uses a generic ImageNet model. For real-world accuracy,
    fine-tune a model on the PlantVillage dataset.
    """
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        
        # Get the top prediction
        top_prediction = decoded_predictions[0]
        imagenet_id, label, score = top_prediction

        # Demo logic: Check if the label contains a keyword we can map
        for keyword, disease_name in CLASS_MAPPING.items():
            if keyword in label.lower():
                return f"{disease_name} (Confidence: {score:.2%})"

        # If no keyword matches, return the top ImageNet class as a fallback
        return f"Could not identify a specific plant disease. Best guess: {label.replace('_', ' ').title()} (Confidence: {score:.2%})"
        
    except Exception as e:
        return f"Error processing image: {str(e)}"
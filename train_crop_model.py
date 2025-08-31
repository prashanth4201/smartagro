# train_crop_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load the dataset
try:
    df = pd.read_csv('Crop_recommendation.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: Crop_recommendation.csv not found. Please download it and place it in the project directory.")
    exit()

# Step 2: Prepare the data
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']
print("Data prepared for training.")

# Step 3: Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

# Step 4: Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("Training Random Forest model...")
model.fit(X_train, y_train)
print("Model training complete.")

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Step 6: Save the trained model
model_filename = 'models/crop_model.pkl'
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")
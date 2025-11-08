import tensorflow as tf
from tensorflow.keras.models import load_model
from pathlib import Path

# Define paths
weights_path = Path(r"C:\Users\samsc\OneDrive\Desktop\AI-Diven Crop Disease Prdiction System\crop_diesease_system\models\saved_models\best_model.h5")

print(f"🔍 Loading full model from: {weights_path}")

try:
    model = load_model(weights_path, compile=False, safe_mode=False)
    print("✅ Model loaded successfully!")
    model.summary()
except Exception as e:
    print(f"❌ Failed to load model: {e}")

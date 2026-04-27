import joblib
import numpy as np
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")

HF_BASE_URL = "https://huggingface.co/arunkakdk/surplux-ml-models/resolve/main"

def download_if_missing(filename):
    filepath = os.path.join(ML_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Downloading {filename} from Hugging Face...")
        r = requests.get(f"{HF_BASE_URL}/{filename}")
        os.makedirs(ML_DIR, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(r.content)
    return filepath

# Load models (downloads from HuggingFace if not present)
model = joblib.load(download_if_missing("food_model.pkl"))
category_encoder = joblib.load(download_if_missing("category_encoder.pkl"))
storage_encoder = joblib.load(download_if_missing("storage_encoder.pkl"))

def predict_shelf_life(category, storage, prep_hour, temp, humidity, quantity):
    category_map = {"cooked": "Cooked", "packaged": "Packaged", "bakery": "Bakery"}
    storage_map = {"room": "Room", "fridge": "Fridge", "freezer": "Freezer"}

    category = category_map.get(str(category).lower(), "Cooked")
    storage = storage_map.get(str(storage).lower(), "Room")

    category_encoded = category_encoder.transform([category])[0]
    storage_encoded = storage_encoder.transform([storage])[0]

    features = [[category_encoded, quantity, storage_encoded, prep_hour, temp, humidity]]
    prediction = model.predict(features)
    return int(prediction[0])
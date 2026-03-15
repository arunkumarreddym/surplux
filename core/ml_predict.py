import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "food_model.pkl")
CATEGORY_ENCODER_PATH = os.path.join(BASE_DIR, "ml", "category_encoder.pkl")
STORAGE_ENCODER_PATH = os.path.join(BASE_DIR, "ml", "storage_encoder.pkl")

model = joblib.load(MODEL_PATH)
category_encoder = joblib.load(CATEGORY_ENCODER_PATH)
print("MODEL CATEGORY LABELS:", category_encoder.classes_)

storage_encoder = joblib.load(STORAGE_ENCODER_PATH)
print("MODEL STORAGE LABELS:", storage_encoder.classes_)
print("Category classes:", category_encoder.classes_)
print("Storage classes:", storage_encoder.classes_)

import numpy as np



def predict_shelf_life(category, storage, prep_hour, temp, humidity, quantity):

    # Match training labels exactly
    category_map = {
        "cooked": "Cooked",
        "packaged": "Packaged",
        "bakery": "Bakery"
    }

    storage_map = {
        "room": "Room",
        "fridge": "Fridge",
        "freezer": "Freezer"
    }

    category = category_map.get(str(category).lower(), "Cooked")
    storage = storage_map.get(str(storage).lower(), "Room")

    # Encode category & storage
    category_encoded = category_encoder.transform([category])[0]
    storage_encoded = storage_encoder.transform([storage])[0]

    # Correct feature order (VERY IMPORTANT)
    features = [[
        category_encoded,   # 1
        quantity,           # 2
        storage_encoded,    # 3
        prep_hour,          # 4
        temp,               # 5  ⭐
        humidity            # 6  ⭐
    ]]

    print("MODEL INPUT:", features)  # Debug

    prediction = model.predict(features)

    print("PREDICTION:", prediction)

    return int(prediction[0])
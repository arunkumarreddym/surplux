import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "ml/food_model.pkl"))
category_encoder = joblib.load(os.path.join(BASE_DIR, "ml/category_encoder.pkl"))
storage_encoder = joblib.load(os.path.join(BASE_DIR, "ml/storage_encoder.pkl"))


def predict_shelf_life(category, quantity, storage, prep_hour, temp, humidity):

    category = category_encoder.transform([category])[0]
    storage = storage_encoder.transform([storage])[0]

    data = np.array([[category, quantity, storage, prep_hour, temp, humidity]])

    prediction = model.predict(data)

    return round(prediction[0], 2)
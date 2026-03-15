import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

print("Loading dataset...")

# Load CSV
df = pd.read_csv("ml/food_data.csv")

print("Columns found:", df.columns)

# Encode category & storage
category_encoder = LabelEncoder()
storage_encoder = LabelEncoder()

df['category'] = category_encoder.fit_transform(df['category'])
df['storage'] = storage_encoder.fit_transform(df['storage'])

# Features & target
X = df[['category','quantity','storage','prep_hour','temp','humidity']]
y = df['safe_hours']

print("Training model...")

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X, y)

print("Saving model...")

joblib.dump(model, "ml/food_model.pkl")
joblib.dump(category_encoder, "ml/category_encoder.pkl")
joblib.dump(storage_encoder, "ml/storage_encoder.pkl")

print("✅ Training Complete!")
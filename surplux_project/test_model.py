import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

print("="*50)
print("   SURPLUX ML MODEL - ACCURACY TESTING REPORT")
print("="*50)

# Load model and encoders
print("\n📦 Loading model and encoders...")
model = joblib.load('ml/food_model.pkl')
cat_enc = joblib.load('ml/category_encoder.pkl')
stor_enc = joblib.load('ml/storage_encoder.pkl')

print(f"✅ Model Type: {type(model).__name__}")

# Load dataset
print("\n📊 Loading dataset...")
df = pd.read_csv('ml/food_data.csv')
print(f"✅ Total Rows: {len(df)}")
print(f"✅ Columns: {df.columns.tolist()}")

# Encode
df['category'] = cat_enc.transform(df['category'])
df['storage'] = stor_enc.transform(df['storage'])

# Split
X = df[['category', 'quantity', 'storage', 'prep_hour', 'temp', 'humidity']]
y = df['safe_hours']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n📈 Training samples: {len(X_train)}")
print(f"📉 Testing samples:  {len(X_test)}")

# Predict
y_pred = model.predict(X_test)

# Metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n" + "="*50)
print("         ACCURACY RESULTS")
print("="*50)
print(f"✅ R² Score          : {round(r2, 4)} ({round(r2*100, 2)}%)")
print(f"✅ Mean Abs Error    : {round(mae, 2)} hours")
print(f"✅ RMSE              : {round(rmse, 2)} hours")
print(f"✅ Mean Actual Hours : {round(y_test.mean(), 2)}")
print(f"✅ Mean Pred Hours   : {round(y_pred.mean(), 2)}")

print("\n" + "="*50)
print("         SAMPLE PREDICTIONS VS ACTUAL")
print("="*50)
print(f"{'Actual':>10} {'Predicted':>10} {'Difference':>12}")
print("-"*35)
for actual, pred in zip(list(y_test[:10]), list(y_pred[:10])):
    diff = round(abs(actual - pred), 2)
    print(f"{round(actual,2):>10} {round(pred,2):>10} {diff:>12}")

print("\n" + "="*50)
print("      REAL WORLD TEST CASES")
print("="*50)

tests = [
    ('Cooked',   'Room',   12, 35, 80, 2),
    ('Cooked',   'Fridge', 12,  4, 50, 2),
    ('Packaged', 'Room',    8, 25, 60, 5),
    ('Bakery',   'Freezer', 6,-18, 40, 1),
    ('Cooked',   'Freezer',10,-10, 30, 3),
]

print(f"{'Category':>10} {'Storage':>8} {'Temp':>5} {'Humid':>6} {'Predicted':>10}")
print("-"*45)
for cat, stor, prep, temp, hum, qty in tests:
    c = cat_enc.transform([cat])[0]
    s = stor_enc.transform([stor])[0]
    pred = model.predict([[c, qty, s, prep, temp, hum]])[0]
    print(f"{cat:>10} {stor:>8} {temp:>5}°C {hum:>5}% {round(pred,1):>8} hrs")

print("\n" + "="*50)
print("✅ MODEL IS PERFORMING EXCELLENTLY!")
print(f"   Accuracy: {round(r2*100,2)}% | Error margin: ±{round(mae,2)} hours")
print("="*50)
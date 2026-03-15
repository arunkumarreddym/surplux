import easyocr
import cv2
import re
from datetime import datetime


reader = easyocr.Reader(['en'])


def read_expiry_and_text(image_path):
    results = reader.readtext(image_path, detail=0)
    text = " ".join(results)

    # find expiry date patterns
    date_pattern = r'(\d{2}[/-]\d{2}[/-]\d{2,4})'
    dates = re.findall(date_pattern, text)

    expiry_date = None

    for d in dates:
        try:
            expiry_date = datetime.strptime(d.replace('/', '-'), "%d-%m-%Y").date()
            break
        except:
            continue

    return expiry_date, text


def detect_product_type(text):
    text = text.lower()

    if "milk" in text:
        return "Milk"
    elif "bread" in text:
        return "Bread"
    elif "juice" in text:
        return "Juice"
    elif "rice" in text:
        return "Rice"
    elif "oil" in text:
        return "Oil"
    else:
        return "General Grocery"


def calculate_days_left(expiry_date):
    if not expiry_date:
        return 0

    today = datetime.today().date()
    return (expiry_date - today).days
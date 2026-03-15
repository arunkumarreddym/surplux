import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text
import re

def extract_details(text):
    lines = text.split("\n")

    name = lines[0]  # usually product name on top

    expiry_date = None
    for line in lines:
        match = re.search(r'(\d{2}/\d{2}/\d{4})', line)
        if match:
            expiry_date = match.group(1)
            break

    return name, expiry_date
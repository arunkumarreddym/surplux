from datetime import datetime

def calculate_discount(mrp, expiry_date_str):
    today = datetime.today().date()
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()

    days_left = (expiry_date - today).days

    # Smart discount rules
    if days_left > 30:
        discount = 5
    elif days_left > 15:
        discount = 15
    elif days_left > 7:
        discount = 30
    elif days_left > 3:
        discount = 50
    else:
        discount = 70

    final_price = mrp - (mrp * discount / 100)

    return days_left, discount, round(final_price, 2)
from datetime import datetime

def check_expiry(expiry):
    today = datetime.now().date()
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()

    if today > expiry_date:
        return "EXPIRED"
    elif (expiry_date - today).days <= 1:
        return "NEAR EXPIRY"
    else:
        return "SAFE"

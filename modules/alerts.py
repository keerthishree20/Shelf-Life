def show_alert(name, status, expiry):
    if status == "EXPIRED":
        print(f"❌ {name} expired on {expiry} - Cannot sell")
    elif status == "NEAR EXPIRY":
        print(f"⚠️ {name} expires soon ({expiry})")
    else:
        print(f"✅ {name} is safe")

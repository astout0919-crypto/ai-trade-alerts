import os
import yfinance as yf
import smtplib
from email.message import EmailMessage

# -------------------
# CONFIGURATION
# -------------------

# Stocks to monitor
STOCKS = ["AAPL", "TSLA", "AMZN"]  # Add your preferred symbols
PRICE_THRESHOLD = 0  # Replace with your alert condition

# GitHub Secrets
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
SMS_GATEWAY = os.environ.get("SMS_GATEWAY")  # e.g., 1234567890@txt.att.net

# -------------------
# FUNCTION TO SEND ALERT
# -------------------

def send_sms_alert(message: str):
    if not EMAIL_USER or not EMAIL_PASS or not SMS_GATEWAY:
        print("Missing email or SMS configuration.")
        return

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Stock Alert"
    msg["From"] = EMAIL_USER
    msg["To"] = SMS_GATEWAY

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# -------------------
# MAIN BOT LOGIC
# -------------------

for ticker in STOCKS:
    try:
        data = yf.Ticker(ticker).history(period="1d")
        last_close = data['Close'][-1]

        # Example alert condition: price > threshold
        if last_close > PRICE_THRESHOLD:
            alert_msg = f"Alert: {ticker} closed at {last_close}"
            print(alert_msg)
            send_sms_alert(alert_msg)

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

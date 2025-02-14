import time
import requests
import re
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load environment variables
load_dotenv()
API_KEY = os.getenv("JUICYSMS_API_KEY")

# Base URL for JuicySMS API
BASE_URL = "https://juicysms.com/api"

# Google Service ID for JuicySMS
SERVICE_ID = "1"

# Country (UK only as required)
COUNTRY = "UK"


def check_balance():
    """Check the account balance in JuicySMS."""
    response = requests.get(f"{BASE_URL}/getbalance?key={API_KEY}").text.strip()
    if response.replace(".", "", 1).isdigit():
        print(f"💰 Account Balance: ${response}")
        return float(response)
    else:
        print("❌ Failed to retrieve account balance:", response)
        return None


def get_phone_number(driver):
    """Request a UK phone number for Google verification and fill it immediately."""
    response = requests.get(f"{BASE_URL}/makeorder?key={API_KEY}&serviceId={SERVICE_ID}&country={COUNTRY}").text.strip()

    match = re.search(r"ORDER_ID_(\d+)_NUMBER_(\d+)", response)
    if match:
        order_id = match.group(1)
        phone_number = f"+44{match.group(2)}"  # Ensure proper format with UK country code
        print(f"📞 Ordered Number: {phone_number} (Order ID: {order_id})")

        # Fill the phone number immediately in Google signup
        try:
            phone_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "phoneNumberId"))
            )
            phone_input.send_keys(phone_number + Keys.ENTER)
            time.sleep(5)  # Wait for Google to process

            print(f"✅ Entered Phone Number: {phone_number}")

        except Exception as e:
            print(f"❌ Error filling phone number in Google signup")
            driver.quit()
            raise

        return order_id, phone_number
    else:
        print(f"❌ Failed to get phone number: {response}")
        return None, None


def get_sms_code(order_id):
    """Retrieve the OTP from SMS for the given order ID."""
    print("⏳ Waiting for OTP...")

    for attempt in range(15):  # Retry every 5 seconds, up to 75 seconds
        response = requests.get(f"{BASE_URL}/getsms?key={API_KEY}&orderId={order_id}").text.strip()

        match = re.search(r"SUCCESS_G-(\d{6})", response)
        if match:
            otp = match.group(1)
            print(f"✅ OTP received: {otp}")
            return otp
        elif "WAITING" in response:
            print(f"🔄 Attempt {attempt + 1}: Still waiting for OTP...")
        else:
            print(f"⚠️ Unexpected response: {response}")
            return None

        time.sleep(5)

    print("❌ OTP retrieval timeout.")
    return None


def cancel_order(order_id):
    """Cancel the phone number order after use or failure."""
    response = requests.get(f"{BASE_URL}/cancelorder?key={API_KEY}&orderId={order_id}").text.strip()
    print(f"🚫 Order Cancellation Response: {response}")


if __name__ == "__main__":
    # Step 1: Check account balance
    check_balance()

    # Step 2: Request a UK number for Google verification and fill it in Google
    order_id, phone_number = get_phone_number()

    if order_id:
        print(f"📢 Use this number: {phone_number} for Google verification.")
        print("📩 Please wait for Google to send OTP...")

        # Step 3: Retrieve OTP
        otp = get_sms_code(order_id)

        if otp:
            print(f"✅ OTP received: {otp}")
        else:
            print("❌ No OTP received.")

        # Step 4: Cancel the order after use
        cancel_order(order_id)
    else:
        print("❌ Could not order a phone number.")

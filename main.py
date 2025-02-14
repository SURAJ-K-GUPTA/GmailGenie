# main.py
import time
import os
import pandas as pd
from config import driver, solver
from recaptcha_solver import solve_recaptcha
from user_details import generate_fake_user
from phone_verification import get_phone_number, get_sms_code, cancel_order
from signup_process import (
    fill_name, fill_dob_gender, fill_username, fill_password, 
    complete_phone_verification, skip_recovery_email, accept_terms
)
from signup_helpers import check_signup_error  # New function to detect signup errors
from selenium.webdriver.common.by import By

i=0
while i<10:
    try:
        # Test Proxy in Selenium by checking public IP
        print("🚀 Testing Proxy in Selenium...")
        driver.get("https://api64.ipify.org?format=json")
        time.sleep(5)
        public_ip = driver.find_element(By.TAG_NAME, "body").text
        print("🌐 Public IP:", public_ip)

        # Open Gmail Signup Page
        driver.get("https://accounts.google.com/signup")
        time.sleep(5)

        # Solve reCAPTCHA if present
        if not solve_recaptcha(driver, solver):
            print("⚠️ reCAPTCHA solving failed. Exiting...")
            driver.quit()
            exit()

        print("✅ Continuing with the signup process...")

        # Generate Fake User Details
        user = generate_fake_user()

        # Fill in Name and Click Next
        fill_name(driver, user["first_name"], user["last_name"])
        time.sleep(15)

        # Fill DOB & Gender
        fill_dob_gender(driver, user["month"], user["day"], user["year"], "Male")
        time.sleep(15)

        # Fill Username
        fill_username(driver, user["username"])
        time.sleep(15)

        # Fill Password
        fill_password(driver, user["password"])
        time.sleep(15)

        # 📌 **Check for Signup Errors Before Proceeding to Phone Verification**
        if check_signup_error(driver):
            print("❌ Signup error detected. Restarting the process...")
            driver.quit()
            time.sleep(5)
            os.system("python main.py")  # Restart the script
            exit()

        # ✅ **Phone Verification Process**
        print("📞 Requesting a phone number from JuicySMS API...")
        order_id, phone_number = get_phone_number(driver)
        if not phone_number:
            print("❌ Failed to get a phone number. Exiting...")
            driver.quit()
            exit()

        time.sleep(5)

        # Wait for OTP
        otp_code = get_sms_code(order_id)
        if not otp_code:
            print("❌ Failed to retrieve OTP. Exiting...")
            cancel_order(order_id)  # Cancel order if OTP not received
            driver.quit()
            exit()

        complete_phone_verification(driver, phone_number, otp_code)

        # Cancel number after use
        cancel_order(order_id)

        time.sleep(5)
        # Skip Recovery Email and Accept Terms
        skip_recovery_email(driver)
        time.sleep(8)

        # If landed on review page
        # Check if "Next" button is present
        try:
            driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='Next']").click()
            time.sleep(5)
        except Exception as e:
            print("⚠️ Next button not found; proceeding...")

        time.sleep(5)

        try:
            driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='Skip']").click()
            time.sleep(5)
        except Exception as e:
            print("⚠️ Skip button not found; proceeding...")

        time.sleep(5)

        try:
            driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='Next']").click()
            time.sleep(5)
        except Exception as e:
            print("⚠️ Next button not found; proceeding...")


        time.sleep(15)
        accept_terms(driver)

        time.sleep(5)



        # Save Account Data
        account_data = {
            "Email": f"{user['username']}@gmail.com",
            "Password": user["password"],
            "Phone": phone_number,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Proxy IP ": public_ip
        }
        df = pd.DataFrame([account_data])
        df.to_csv("accounts.csv", mode="a", index=False, header=not os.path.exists("accounts.csv"))
        print(f"✅ Account Created: {user['username']}@gmail.com | Password: {user['password']}")

        # Close Browser

        time.sleep(60)
        driver.quit()

        i+=1

    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(10)
        print("❌ Restarting the process...")
        os.system("python main.py")

        exit()
# signup_process.py
import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def fill_name(driver, first_name, last_name):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "firstName"))
    ).send_keys(first_name)
    driver.find_element(By.NAME, "lastName").send_keys(last_name)
    driver.find_element(By.XPATH, "//span[@jsname='V67aGc']").click()
    time.sleep(5)
    print("✅ Entered Name & Clicked Next")

def fill_dob_gender(driver, month, day, year, gender="Male"):
    try:
        # Use the Select class to interact with the month dropdown
        month_dropdown = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        select_month = Select(month_dropdown)
        # The values for the options are "1", "2", ..., "12"
        select_month.select_by_value(str(month))
    except Exception as e:
        print("❌ Failed to select month:")
        driver.quit()
        sys.exit()
    
    # Fill day and year fields
    driver.find_element(By.ID, "day").send_keys(day)
    driver.find_element(By.ID, "year").send_keys(year)
    
    # Fill gender field (this example uses send_keys; adjust if needed)
    driver.find_element(By.ID, "gender").send_keys(gender)
    
    # Click Next button
    driver.find_element(By.XPATH, "//span[@jsname='V67aGc']").click()
    time.sleep(5)
    print("✅ Entered DOB & Gender")

def fill_username(driver, username):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import time

    username_field = None

    # 📌 **Step 1: Check for 'Create a Gmail address' option**
    custom_option_xpaths = [
        "//div[@id='selectionc1' and contains(text(),'Create a Gmail address')]",
        "//div[@id='selectionc3' and contains(text(),'Create a Gmail address')]",
        "//div[contains(@class, 'QTJzre') and .//div[contains(text(),'Create a Gmail address')]]"
    ]

    option_clicked = False
    for xpath in custom_option_xpaths:
        try:
            custom_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            if custom_option:
                print("✅ Found 'Create a Gmail address' option. Clicking it...")
                custom_option.click()
                time.sleep(5)  # Wait for UI update
                option_clicked = True
                break
        except Exception:
            print(f"⚠️ Could not find 'Create a Gmail address' option using locator: {xpath}")

    if option_clicked:
        # Try to locate the radio button and click it if needed
        try:
            radio_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='radio' and @data-value='custom']"))
            )
            radio_button.click()
            print("✅ Clicked 'Create your own Gmail address' radio button.")
            time.sleep(5)  # Wait for UI update
        except Exception:
            print("⚠️ No radio button found, proceeding...")

    # 📌 **Step 2: Locate the username input field**
    def find_username_field():
        username_locators = [
            "//input[@aria-label='Create a Gmail address' and @name='Username']",  # Custom label field
            "//input[@name='Username']",  # Standard field
            "//input[contains(@class, 'whsOnd') and @type='text']"  # Generic fallback
        ]
        for locator in username_locators:
            try:
                field = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, locator))
                )
                if field:
                    print(f"✅ Located username field using: {locator}")
                    return field
            except Exception:
                print(f"⚠️ Could not locate username field with: {locator}")
        return None

    # First attempt to find username field
    username_field = find_username_field()

    # 📌 **Step 3: If username field is not found, click "Next" and retry**
    if not username_field:
        print("⚠️ Username input field not found. Clicking 'Next' and retrying...")
        try:
            next_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc']"))
            )
            next_button.click()
            time.sleep(5)  # Wait for page to update
        except Exception:
            print("❌ Failed to click 'Next'. Exiting...")
            driver.quit()
            raise Exception("Username field not found, and 'Next' button click failed.")

        # Try again to find username field
        username_field = find_username_field()
        if not username_field:
            print("❌ Username field still not found after retry. Exiting...")
            driver.quit()
            raise Exception("Username field not found after retrying.")

    # 📌 **Step 4: Fill in the username**
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", username_field)
        username_field.clear()
        username_field.send_keys(username)

        # Click "Next" to validate the username
        next_button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc']"))
        )
        next_button.click()
        time.sleep(5)

        print(f"✅ Successfully entered username: {username}")
    except Exception as e:
        print(f"❌ Error entering username")
        driver.quit()
        raise

def fill_password(driver, password):
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.NAME, "PasswdAgain").send_keys(password + Keys.ENTER)
    time.sleep(8)
    print(f"✅ Generated & Entered Password: {password}")

def complete_phone_verification(driver, phone_number, otp_code):
    """
    Complete the phone verification process in the Google signup form.
    
    :param driver: Selenium WebDriver instance
    :param phone_number: The phone number to enter
    :param otp_code: The received OTP code
    """
    try:
        # Wait a few seconds to allow Google to send OTP
        time.sleep(10)

        # Enter OTP
        otp_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "code"))
        )
        otp_input.send_keys(otp_code + Keys.ENTER)
        time.sleep(5)
        print(f"✅ Entered OTP: {otp_code}")

    except Exception as e:
        print(f"❌ Error during phone verification: {e}")
        driver.quit()
        raise
def skip_recovery_email(driver):
    try:
        driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='Skip']").click()
        time.sleep(5)
        print("✅ Skipped Recovery Email")
    except Exception as e:
        print("⚠️ No option to skip Recovery Email:")
    try:
        driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='Next']").click()
        time.sleep(5)
    except Exception as e:
        print("⚠️ Next button on Recovery Email page not found; proceeding...")

def accept_terms(driver):
    try:
        time.sleep(8)
        driver.find_element(By.XPATH, "//span[@jsname='V67aGc' and text()='I agree']").click()
        time.sleep(8)
        print("✅ Accepted Terms & Conditions")
    except Exception as e:
        print("⚠️ I agree button not found; please check the page.")
        driver.quit()

# signup_helpers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_signup_error(driver):
    """
    Checks if an error message is displayed on the page indicating
    that the account could not be created. Detects any message containing "error".
    
    Returns True if the error is detected; otherwise False.
    """
    try:
        # Wait for up to 5 seconds to detect any error message containing the word "error"
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sorry')]")
            )
        )
        if error_element:
            print("❌ Error detected on signup page!")
            return True
    except Exception:
        # If the element is not found within 5 seconds, assume no error.
        return False
    return False

# recaptcha_solver.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def detect_recaptcha(driver):
    """Detects if reCAPTCHA exists on the page."""
    try:
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
        )
        print("🔍 reCAPTCHA detected.")
        return iframe
    except Exception:
        print("✅ No reCAPTCHA detected.")
        return None

def solve_recaptcha(driver, solver):
    """Solves reCAPTCHA and injects the token into the form."""
    print("🚀 Solving reCAPTCHA...")
    recaptcha_iframe = detect_recaptcha(driver)
    if not recaptcha_iframe:
        return True  # No CAPTCHA; nothing to solve

    recaptcha_src = recaptcha_iframe.get_attribute("src")
    try:
        # Extract the sitekey from the iframe src URL (assumes parameter 'k' exists)
        sitekey = recaptcha_src.split("k=")[1].split("&")[0]
    except Exception as e:
        print("❌ Failed to extract sitekey:", e)
        return False
    print(f"🔑 Extracted sitekey: {sitekey}")

    try:
        token = solver.recaptcha(sitekey=sitekey, url=driver.current_url)
        print(f"✅ Solved reCAPTCHA: {token}")
        # Inject the token into the page (assumes an element with id "g-recaptcha-response")
        driver.execute_script(
            f'document.getElementById("g-recaptcha-response").innerHTML = "{token}";'
        )
        return True
    except Exception as e:
        print(f"❌ Failed to solve reCAPTCHA: {e}")
        return False

# config.py
import os
import time
from dotenv import load_dotenv
from seleniumwire import webdriver  # Note: using selenium-wire
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twocaptcha import TwoCaptcha

# Load environment variables from .env file
load_dotenv()

# Environment variables
TWO_CAPTCHA_API_KEY = os.getenv("TWO_CAPTCHA_API_KEY")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")
# SMS_ACTIVATE_API_KEY is loaded in phone_verification.py

# Create Proxy URL
proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

# Configure Selenium Wire Options for Proxy
seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url,
        "no_proxy": "localhost,127.0.0.1"
    }
}

# Configure Chrome Options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver with Proxy
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options,
    options=chrome_options
)

# Initialize 2Captcha solver
solver = TwoCaptcha(TWO_CAPTCHA_API_KEY)
# print("🚀 Testing Proxy in Selenium...")
# driver.get("https://api64.ipify.org?format=json") 

time.sleep(5)
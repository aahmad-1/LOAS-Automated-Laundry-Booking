from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Get user credentials
print("=== LOAS Laundry Booking Bot ===")
email = input("Enter your email: ")
password = input("Enter your password: ")

chrome_options = Options()
chrome_options.add_argument("--lang=en") 

service = Service("C:\\WebDriver\\chromedriver-win64\\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.maximize_window()

def initialize_browser():
    try:
        # Navigate to login page
        print("\nNavigating to login page...")
        browser.get("https://intra.loas.fi/bookings")
        
        # Wait for the email input field to be present
        wait = WebDriverWait(browser, 10)
        
        print("Entering email...")
        email_field = wait.until(
            EC.presence_of_element_located((By.ID, "customer_email")))
        email_field.clear()
        email_field.send_keys(email)
        
        print("Entering password...")
        password_field = browser.find_element(By.ID, "customer_password")
        password_field.clear()
        password_field.send_keys(password)
        
        print("Clicking login button...")
        login_button = browser.find_element(By.CSS_SELECTOR, "input[value='Kirjaudu sisään']")
        login_button.click()
        
        # Wait for redirect to booking page
        print("Waiting for redirect...")
        wait.until(EC.url_contains("/complexes/"))
        
        print(f"✓ Successfully logged in!")
        print(f"Current URL: {browser.current_url}")
        
        time.sleep(5)
        
    except Exception as e:
        print(f"✗ Error occurred: {str(e)}")
        
    finally:
        # Uncomment this when you want the browser to close automatically
        # driver.quit()
        pass

initialize_browser()
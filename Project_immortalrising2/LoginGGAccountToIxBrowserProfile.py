'''
Status: Successfully Run ---- for profile no proxy if the profile have proxy the code run really slow
Purpose: Login Google account in ixBrowser Profile
Owner: Thuong
Date Done: 11:54am 12.12.2024

Notes: Login directly using gmail + password
if having recover email, comfirm message,there is in need to update the code
kernel: 114
chromedriver 114
'''
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_driver(debugging_address):
    """Initialize Selenium WebDriver with a debugging address."""
    options = webdriver.ChromeOptions()
    options.debugger_address = debugging_address

    # Specify the path to the local chromedriver binary
    chromedriver_path = os.path.join(os.getcwd(),'chromedriver_win32_114\\chromedriver.exe')
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"chromedriver not found at {chromedriver_path}")
    return webdriver.Chrome(service=Service(chromedriver_path), options=options)

def create_new_tab(driver):
    """Create and switch to a new tab."""
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    logging.info("New tab created and focused.")

def search_google(driver):
    """Perform a Google search."""
    try:
        driver.get("https://www.google.com")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("https://accounts.google.com/")
        search_box.send_keys(Keys.RETURN)
        logging.info("Search for 'account' executed.")
    except Exception as e:
        logging.error(f"Error during Google search: {e}")

def login_gmail(driver, email, password, recovery_email=None):
    """Automate Gmail login process."""
    try:
        driver.get("https://accounts.google.com/")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "identifierId"))
        ).send_keys(email, Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        ).send_keys(password, Keys.RETURN)
        logging.info("Logged in to Gmail.")

        if recovery_email:
            try:
                # Check if the recovery email confirmation is required
                confirm_recovery_prompt = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Confirm your recovery email')]")
                ))
                if confirm_recovery_prompt.is_displayed():
                    logging.info("Recovery email confirmation prompt detected.")

                    # Fill the recovery email
                    recovery_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@id='knowledge-preregistered-email-response']")
                    ))
                    recovery_field.send_keys(recovery_email)

                    # Click the Next button
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")
                    ))
                    next_button.click()
                    logging.info("Recovery email provided and Next button clicked.")

            except Exception as e:
                logging.info(f"Recovery email prompt not detected or handled: {e}")
    except Exception as e:
        logging.error(f"Error during Gmail login: {e}")

def open_profile(profile_id):
    """Open ixBrowser profile via API and return debugging details."""
    api_url = "http://127.0.0.1:53200/api/v2/profile-open"
    headers = {"Content-Type": "application/json"}
    data = {
        "profile_id": profile_id,
        "args": ["--disable-extension-welcome-page"],
        "load_extensions": True,
        "load_profile_info_page": True,
        "cookies_backup": True,
        "cookie": ""
    }

    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("error", {}).get("code") == 0:
            return response_data["data"]["debugging_address"]
        else:
            raise Exception(f"API error: {response_data['error']['message']}")
    else:
        raise Exception("Failed to open profile via API.")

# Main execution
try:
    profile_id = 1145  # Replace with your profile ID
    debugging_address = open_profile(profile_id)
    logging.info(f"Profile debugging address: {debugging_address}")

    driver = initialize_driver(debugging_address)
    try:
        create_new_tab(driver)  # Open and switch to a new tab
        search_google(driver)  # Perform the Google account search

        email = os.getenv("GMAIL_EMAIL", "anhmongdieuu11@gmail.com")
        password = os.getenv("GMAIL_PASSWORD", "anhmongdieuu1503@#")
        recovery_email = os.getenv("GMAIL_RECOVERY_EMAIL", "roycallahan531338@hotmail.com")
        login_gmail(driver, email, password, recovery_email=recovery_email)
    finally:
        driver.quit()
except Exception as e:
    logging.error(f"Error: {e}")




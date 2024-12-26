import time
import os
import imaplib
import email
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Optional: Automates Chromedriver download
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Email Handler for verification codes
class EmailHandler:
    def __init__(self, imap_host, email_user, email_password):
        self.imap_host = imap_host
        self.email_user = email_user
        self.email_password = email_password

    def fetch_verification_code(self, subject_filter="Verification Code"):
        retries = 3
        for attempt in range(retries):
            try:
                with imaplib.IMAP4_SSL(self.imap_host) as mail:
                    mail.login(self.email_user, self.email_password)
                    mail.select("inbox")
                    status, email_ids = mail.search(None, f'(SUBJECT "{subject_filter}")')
                    if status == "OK" and email_ids[0]:
                        email_id = email_ids[0].split()[-1]
                        status, data = mail.fetch(email_id, "(RFC822)")
                        msg = email.message_from_bytes(data[0][1])
                        body = self.extract_email_body(msg)
                        verification_code = next((line for line in body.split("\n") if line.isdigit()), None)
                        if verification_code:
                            return verification_code
                    else:
                        logging.info("No matching emails found. Retrying...")
            except Exception as e:
                logging.error(f"Error during email fetch: {e}")
            time.sleep(10)  # Wait before retrying
        return None

    def extract_email_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode()
                elif content_type == "text/html":
                    # Extract HTML content and remove tags if necessary
                    html_content = part.get_payload(decode=True).decode()
                    return BeautifulSoup(html_content, "html.parser").get_text()
        else:
            return msg.get_payload(decode=True).decode()


# Open the iXBrowser profile
def open_ixbrowser_profile(profile_id):
    api_url = "http://127.0.0.1:53200/api/v2/profile-open"
    payload = {
        "profile_id": profile_id,
        "args": ["--disable-extensions"],
        "load_extensions": True,
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("error", {}).get("code") == 0:
            logging.info("iXBrowser profile opened successfully.")
            return data["data"]["debugging_address"]
        else:
            logging.error(f"iXBrowser API Error: {data['error']['message']}")
    else:
        logging.error(f"Failed to connect to iXBrowser API with status code {response.status_code}.")
    return None


# Initialize Selenium Driver
def initialize_driver(chromedriver_path, debugging_address=None):
    try:
        options = webdriver.ChromeOptions()
        if debugging_address:
            options.debugger_address = debugging_address
        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Selenium WebDriver connected successfully.")
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise


# Automating ImmortalRising2 sign-up and verification code input
# Automating ImmortalRising2 sign-up and verification code input
# Automating ImmortalRising2 sign-up and verification code input
# Automating ImmortalRising2 sign-up and verification code input
def automate_certik_signup(driver, email, password, email_handler):
    try:
        # Save the current window handle
        original_window = driver.current_window_handle

        # Open the sign-up page
        driver.get("https://immortalrising2.com/?referral=tQnb8qToyl")

        # Click sign-in
        signin_xpath = "//button[normalize-space()='Sign in']"
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, signin_xpath))
        )
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, signin_xpath))
        ).click()

        # Wait for and click the email input field
        email_input_xpath = "//span[@class='text-button2 whitespace-nowrap text-gray-900']"
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, email_input_xpath))
        )
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, email_input_xpath))
        ).click()

        # Wait for the new window/tab to open
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Switch to the new window
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        logging.info("Switched to new window.")

        # Interact with the email input field
        email_input_xpath = "//input[@type='email']"  # Corrected variable name
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.XPATH, email_input_xpath))
        )
        WebDriverWait(driver, 90).until(
            EC.element_to_be_clickable((By.XPATH, email_input_xpath))
        ).send_keys(email)

        # Wait for the next interaction, e.g., consent checkbox or continue button
        consent_button_xpath = "//input[@id='marketingConsent']"
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, consent_button_xpath))
        )
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, consent_button_xpath))
        ).click()

        # Submit the code after input
        submit_button_xpath = "//button[@type='submit']"
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, submit_button_xpath))
        )
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, submit_button_xpath))
        ).click()

        # Wait for the verification email and extract the code
        verification_code = email_handler.fetch_verification_code()

        if verification_code:
            # Enter the verification code into the fields
            for i, digit in enumerate(verification_code[:6]):
                input_xpath = f"//div[@id='passwordless_container']//div[{i + 1}]//input[1]"
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, input_xpath))
                )
                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, input_xpath))
                ).send_keys(digit)



            logging.info("Sign-up completed successfully.")
        else:
            logging.error("No verification code found in email.")
    except Exception as e:
        logging.error(f"Error in sign-up automation: {e}")
        raise






# Main
if __name__ == "__main__":
    # User Credentials
    EMAIL_USER = "ovtrzpyu@esponamail.com"  # Replace with your email
    EMAIL_PASS = "xeibdbncY4994"  # Replace with your password
    EMAIL_IMAP = "imap.firstmail.ltd"  # Adjust for your email provider
    PROFILE_ID = 10  # Replace with your iXBrowser profile ID

    email_handler = EmailHandler(EMAIL_IMAP, EMAIL_USER, EMAIL_PASS)

    # Ensure correct ChromeDriver is specified
    CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver_win32_114\\chromedriver.exe')  # Adjust as needed
    debugging_address = open_ixbrowser_profile(PROFILE_ID)
    driver = None
    if debugging_address:
        driver = initialize_driver(CHROMEDRIVER_PATH, debugging_address)
    else:
        driver = initialize_driver(CHROMEDRIVER_PATH)  # Default WebDriver

    if driver:
        try:
            test_email = "ovtrzpyu@esponamail.com"  # Replace with your test email
            test_password = "xeibdbncY4994"  # Replace with your test password
            automate_certik_signup(driver, test_email, test_password, email_handler)
        finally:
            driver.quit()
    else:
        logging.error("Failed to initialize ChromeDriver session.")

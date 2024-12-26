
'''
update SignUpReferal
Status: Run 70%
Currently: I cant not import the getverifycode and extract the code number to automatical fill in the blank
'''
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


class EmailHandler:
    def __init__(self, username, password, imap_server='imap.firstmail.ltd', imap_port=993):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port

    def read_email_from_certik(self, expected_sender='hello@passport.e.immutable.com'):
        """
        Reads the email from the given sender and extracts the verification code.
        """
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.username, self.password)
            mail.select('inbox')
            _, search_data = mail.search(None, 'ALL')
            email_ids = search_data[0].split()

            # Iterate through emails (newest first)
            for email_id in reversed(email_ids):
                _, email_data = mail.fetch(email_id, '(RFC822)')
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                sender = email.utils.parseaddr(email_message['From'])[1]
                if sender == expected_sender:
                    # Extract body from the email
                    body = self.extract_body_from_email(email_message)
                    verification_code = self.extract_verification_code(body)
                    mail.close()
                    mail.logout()
                    return body  # Instead of returning verification_code

            print("No matching emails found.")
            mail.close()
            mail.logout()
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def extract_body_from_email(self, email_message):
        """
        Extracts the email body content.
        """
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode()
                elif content_type == "text/html":
                    return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()

    def extract_verification_code(self, email_body):
        """
        Extracts a 6-digit verification code.
        """
        verification_code_pattern = r'(\d{6})'
        matches = re.findall(verification_code_pattern, email_body)
        if matches:
            print("Found the following 6-digit codes: ", matches)
            return matches[0]
        else:
            print("No 6-digit verification code found.")
            return None


# Function usage example
def get_verification_code_from_email():
    # Replace with actual email credentials
    username = 'tmouylqd@puercomail.com'
    password = 'cvfdwnjrS7744'
    email_handler = EmailHandler(username, password)

    # Extract verification code from the specific email address
    email_body = email_handler.read_email_from_certik()
    verification_code = email_handler.extract_verification_code(email_body) if email_body else None

    if verification_code:
        print(f"Verification code: {verification_code}")
    else:
        print("Could not retrieve the verification code.")


# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
def automate_certik_signup(driver, email, password, email_handler):
    try:
        original_window = driver.current_window_handle

        # Open the sign-up page
        driver.get("https://immortalrising2.com/?referral=tQnb8qToyl")

        # Sign in
        signin_xpath = "//button[normalize-space()='Sign in']"
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, signin_xpath)))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, signin_xpath))).click()

        # Click email input
        email_input_xpath = "//span[@class='text-button2 whitespace-nowrap text-gray-900']"
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, email_input_xpath)))
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, email_input_xpath))).click()

        # Wait for and switch to the new window
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        logging.info("Switched to new window.")

        # Fill in the email
        email_input_xpath = "//input[@type='email']"
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, email_input_xpath)))
        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.XPATH, email_input_xpath))).send_keys(email)

        # Accept marketing consent
        consent_button_xpath = "//input[@id='marketingConsent']"
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, consent_button_xpath)))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath))).click()

        # Submit form
        submit_button_xpath = "//button[@type='submit']"
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, submit_button_xpath)))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath))).click()

######################################################################################
        # Wait for verification code
        verification_code = email_handler.extract_verification_code()
        if verification_code:
            # Enter the verification code
            for i, digit in enumerate(verification_code[:6]):
                input_xpath = f"//div[@id='passwordless_container']//div[{i + 1}]//input[1]"
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, input_xpath))).send_keys(digit)

            logging.info("Sign-up completed successfully.")
        else:
            logging.error("No verification code found in email.")
    except Exception as e:
        logging.error(f"Error in sign-up automation: {e}")
        raise


# Main execution block
if __name__ == "__main__":
    # User Credentials
    EMAIL_USER = "tmouylqd@puercomail.com"
    EMAIL_PASS = "cvfdwnjrS7744"
    EMAIL_IMAP = "imap.firstmail.ltd"
    PROFILE_ID = 15

    email_handler = EmailHandler(EMAIL_IMAP, EMAIL_USER, EMAIL_PASS)

    # Ensure correct ChromeDriver is specified
    CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver_win32_114\\chromedriver.exe')
    debugging_address = open_ixbrowser_profile(PROFILE_ID)
    driver = None
    if debugging_address:
        driver = initialize_driver(CHROMEDRIVER_PATH, debugging_address)
    else:
        driver = initialize_driver(CHROMEDRIVER_PATH)

    if driver:
        try:
            automate_certik_signup(driver, EMAIL_USER, EMAIL_PASS, email_handler)
        finally:
            driver.quit()
    else:
        logging.error("Failed to initialize ChromeDriver session.")

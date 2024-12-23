'''
Status: Successfully Run 100%
- error - go to the Claim button
- I think we should reorder the task as it based on ưu tiên và thứ tự
- have not connect to save to database
- can improve the button and parent css using better code structure {i}

Required: already login imap account to immortalrising2.com
'''
import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_task_page(driver, task_url="https://immortalrising2.com/mission"):
    """Navigate to the Mission page."""
    try:
        driver.get(task_url)
        logging.info(f"Navigating to {task_url}")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='MISSION']"))
        )
        logging.info("Mission page loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading the Mission page: {e}")
        raise

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to your Chromedriver (ensure version compatibility)
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver_win32_114\\chromedriver.exe')  # Adjust as needed

def open_ixbrowser_profile(profile_id):
    """Open iXBrowser profile using the API and return debugging address."""
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
            logging.error(f"Error from iXBrowser API: {data['error']['message']}")
    else:
        logging.error("Failed to connect to iXBrowser API.")
    return None

def initialize_driver(debugging_address):
    """Initialize Selenium WebDriver and connect to iXBrowser instance."""
    options = webdriver.ChromeOptions()
    options.debugger_address = debugging_address
    service = webdriver.chrome.service.Service(CHROMEDRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Selenium WebDriver connected to iXBrowser.")
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise

def find_and_execute_task(driver):
    """Scan for tasks dynamically, match parent element to "Go" button, and execute the first task found."""
    try:
        # Parent elements XPaths
        PARENT_XPATHS = [
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(8) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(9) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(10) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(11) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(12) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(13) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(14) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(15) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(16) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(17) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(18) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(19) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(20) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(21) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(22) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",
            "body > main:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(23) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)",

        ]
        # Corresponding Go button XPaths
        GO_BUTTON_XPATHS = [
        "(// button[contains(text(), 'Claim')])[1]",
        "(//button[@class='flex justify-center items-center rounded-[4px] bg-primary-600 text-primary-25 *:fill-primary-100 hover:bg-primary-25 hover:text-primary-900 *:hover:fill-primary-700 disabled:bg-primary-300 disabled:text-primary-100 *:disabled:fill-primary-100 relative flex justify-center items-center rounded-[4px] h-[36px] px-[16px] py-[8px] text-button3 gap-[4px] *:*:w-[20px] *:*:h-[20px] min-w-[73px]'][normalize-space()='Claim'])[2]",
        "(// button[contains(text(), 'Claim')])[3]",
        "(// button[contains(text(), 'Claim')])[4]",
        "(// button[contains(text(), 'Claim')])[5]",
        "(// button[contains(text(), 'Claim')])[6]",
        "(// button[contains(text(), 'Claim')])[7]",
        "(// button[contains(text(), 'Claim')])[8]",
        "(// button[contains(text(), 'Claim')])[9]",
        "(// button[contains(text(), 'Claim')])[10]",
        "(// button[contains(text(), 'Claim')])[11]",
        "(// button[contains(text(), 'Claim')])[12]",
        "(// button[contains(text(), 'Claim')])[13]",
        "(// button[contains(text(), 'Claim')])[14]",
        "(// button[contains(text(), 'Claim')])[15]",
        "(// button[contains(text(), 'Claim')])[16]",
        "(// button[contains(text(), 'Claim')])[17]",
        "(// button[contains(text(), 'Claim')])[18]",
        "(// button[contains(text(), 'Claim')])[19]",
        "(// button[contains(text(), 'Claim')])[20]",
        "(// button[contains(text(), 'Claim')])[21]",
        "(// button[contains(text(), 'Claim')])[22]",
        "(// button[contains(text(), 'Claim')])[23]"
        ]

        # Task list
        '''
//p[normalize-space()='Sign up and claim your first reward']
//p[normalize-space()='Enter referral code in 24H']
//p[normalize-space()='Bring Your Own Friend']
//p[normalize-space()='Connect Immutable Passport']
//p[normalize-space()='Download & Play IR2!']
//p[normalize-space()='Join the Official IR2 Discord']
//p[normalize-space()='Follow @ImmortalRising2 on X']
//p[normalize-space()='Join the Official IR2 Telegram']
//p[normalize-space()='Subscribe to IR2 Newsletter']
//p[normalize-space()='Reach Soulstone Level 12']
//p[normalize-space()='Awakening - SS']
//p[normalize-space()='Awakening - SSS']
//p[normalize-space()='Complete All Dungeons (Lv 40)']
//p[normalize-space()='Conqueror of Hell']
//p[normalize-space()='Complete SSS Gear Setup']
//p[normalize-space()='Reach Soulstone Level 18']
//p[normalize-space()='Spend 5000 Stardust']
//p[normalize-space()='Join Open Meta DAO Discord']
//p[normalize-space()='Visit Terminal']
//p[normalize-space()='Follow Everreach Labs on X']
//p[normalize-space()='Follow SMOK3 on X']




(//p[normalize-space()="Like, RT, Comment SMOK3's tweet"])[1] #tìm nút riêng cho hai task này
(//p[normalize-space()="Like, RT, Comment Emergence's tweet"])[1]''' #tìm nút riêng cho hai task này
        TASKS = [
            "Sign up and claim your first reward",
            "Enter referral code in 24H",
            "Bring Your Own Friend",
            "Connect Immutable Passport",
            "Download & Play IR2!",
            "Join the Official IR2 Discord",
            "Follow @ImmortalRising2 on X",
            "Join the Official IR2 Telegram",
            "Subscribe to IR2 Newsletter",
            "Reach Soulstone Level 12",
            "Awakening - SS",
            "Awakening - SSS",
            "Complete All Dungeons (Lv 40)",
            "Conqueror of Hell",
            "Complete SSS Gear Setup",
            "Reach Soulstone Level 18",
            "Spend 5000 Stardust",
            "Join Open Meta DAO Discord",
            "Visit Terminal",
            "Follow Everreach Labs on X",
            "Follow SMOK3 on X"
        ]

        for i, parent_xpath in enumerate(PARENT_XPATHS):
            try:
                parent_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, parent_xpath))
                )

                found_task = False
                task_name = None

                # Check for matching task within this parent
                for task in TASKS:
                    task_xpath = f".//p[normalize-space()='{task}']"  # XPath động
                    if parent_element.find_elements(By.XPATH, task_xpath):
                        logging.info(f"Found task '{task}' inside parent element: {parent_xpath}.")
                        found_task = True
                        task_name = task
                        break

                if found_task:
                    # Execute task with corresponding Go button
                    go_xpath = GO_BUTTON_XPATHS[i]
                    logging.info(f"Executing task: {task_name}")
                    navigate_and_execute(driver, go_xpath)
                    return  # Exit after executing the first task

            except Exception as e:
                logging.error(f"Error processing parent element {parent_xpath}: {e}")

        logging.info("No matching tasks found in any parent element.")

    except Exception as e:
        logging.error(f"Error finding or executing task: {e}")
        raise

def navigate_and_execute(driver, go_xpath):
    """Navigate to an element given the XPath."""
    try:
        navigate_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, go_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(navigate_element).click().perform()
        logging.info("Successfully navigated to the 'Claim' button.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Error navigating to 'Go' button: {e}")

def main():
    profile_id = 1027  # Replace with your iXBrowser profile ID
    debugging_address = open_ixbrowser_profile(profile_id)

    if debugging_address:
        driver = initialize_driver(debugging_address)
        try:
            navigate_to_task_page(driver)  # Open daily tasks page
            find_and_execute_task(driver)  # Execute predefined tasks
        finally:
            logging.info("Browser session closed.")
            driver.quit()
    else:
        logging.error("Failed to retrieve debugging address from iXBrowser.")

if __name__ == "__main__":
    main()

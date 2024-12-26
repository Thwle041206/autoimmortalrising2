'''
Status: Successful Run
Purpose: Creating a Browser - API
Owner: Thuong
Date Done: 10:08am 10.12.2024

Code Process:
Load Proxies: Reads proxy details from a file.
User Input: Asks for the number of profiles and group name.
Validate Input: Checks input validity.
Create Profiles: Configures and sends API requests to create profiles.
Handle Responses: Displays success or error messages.
Error Handling: Manages and reports request errors.

Sources: https://www.ixbrowser.com/doc/v2/local-api/cn?target_id=7c9a2293-04aa-4d9f-b102-be4249357bdc
'''
import requests
import json

# API URL and API Key
API_URL = "http://127.0.0.1:53200/api/v2/profile-create"
API_UPDATE_URL = "http://127.0.0.1:53200/api/v2/profile-update"
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Load proxies from file
PROXY_FILE = "proxies.txt"

def load_proxies(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]

proxies = load_proxies(PROXY_FILE)

# Predefined group name
GROUP_NAME = "Default Group"  # Replace with your desired group name

# Get user input for the number of profiles
try:
    num_profiles = int(input("How many profiles do you want to create? "))
    if num_profiles <= 0:
        print("Number of profiles must be greater than zero.")
        exit()
except ValueError:
    print("Please enter a valid number.")
    exit()

# Iterate over proxies to create browser profiles
for i in range(1, num_profiles + 1):
    proxy = proxies[(i - 1) % len(proxies)]  # Cycle through proxies if needed
    proxy_parts = proxy.split(":")
    proxy_host = proxy_parts[0]
    proxy_port = int(proxy_parts[1])
    proxy_username = proxy_parts[2] if len(proxy_parts) > 2 else ""
    proxy_password = proxy_parts[3] if len(proxy_parts) > 3 else ""

    # Configuration for creating a browser
    browser_config = {
        "name": f"profile{i}",  # Temporary name
        "group": GROUP_NAME,  # Predefined group name
        "os": "windows",
        "proxy": {
            "type": "http",
            "host": proxy_host,
            "port": proxy_port,
            "username": proxy_username,
            "password": proxy_password,
        },
        "screen_resolution": "1920x1080",
        "timezone": "America/New_York",
        "webgl": True,
        "canvas": True,
    }

    try:
        # Sending the POST request
        response = requests.post(API_URL, headers=headers, data=json.dumps(browser_config))
        if response.status_code == 200:
            response_data = response.json()
            profile_id = response_data["data"]
            print(f"Browser profile created successfully with ID {profile_id}!")

            # Update the profile name to include its ID
            update_config = {
                "id": profile_id,
                "name": f"profile{profile_id}",  # Name format: profile + ID
            }
            update_response = requests.post(API_UPDATE_URL, headers=headers, data=json.dumps(update_config))
            if update_response.status_code == 200:
                print(f"Profile name updated to 'profile{profile_id}' successfully!")
            else:
                print(f"Failed to update profile name for ID {profile_id}.")
                print("Response:", update_response.text)
        else:
            print(f"Failed to create browser profile. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating profile {i}:", e)

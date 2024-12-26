"""
Status: Successful
Update 1 browser

Need to improve to update a range of browser or a group later
"""
import requests
import json

# Define the URL for the API
url = "http://127.0.0.1:53200/api/v2/profile-update"

# Define the updated data with only the kernel version and browser version set
data = {
    "profile_id": 10,  # Provide your profile_id
    "fingerprint_config": {
        "kernel_version": "114",  # Update kernel_version to 114
        "br_version": "114",      # Update browser version to 114
    }
}

# Set the headers for the API request
headers = {
    "Content-Type": "application/json"
}

# Send a POST request to the API
response = requests.post(url, json=data, headers=headers)

# Check the response status and print the result
if response.status_code == 200:
    print("Profile updated successfully.")
    print(response.json())  # Print the response from the API
else:
    print(f"Failed to update profile. Status code: {response.status_code}")
    print(response.text)  # Print the error message if any

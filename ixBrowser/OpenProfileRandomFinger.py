"""
Status: Error 
"""import requests

def open_browser_with_random_fingerprint():
    url = "http://127.0.0.1:53200/api/v2/profile-open-with-random-fingerprint"

    # Payload configuration without proxy
    payload = {
        "profile_id": 1045,
        "args": [
            "--disable-extension-welcome-page"
        ],
        "load_profile_info_page": True,
        "fingerprint_config": {
            "hardware_concurrency": "4",
            "device_memory": "8",
            "ua_type": 1,
            "platform": "Windows",
            "ua_info": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "kernel_version": "0",
            "language_type": "1",
            "timezone_type": "1",
            "timezone": "Asia/Shanghai",
            "location": "1",
            "location_type": "1",
            "longitude": 25.7247,
            "latitude": 119.3712,
            "accuracy": 1000,
            "resolving_power_type": "2",
            "resolving_power": "500,500",
            "webgl_image": "1",
            "audio_context": "1",
            "speech_voices": "1"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    try:
        response = requests.post(url, json=payload, headers=headers)

        # Handle the response
        if response.status_code == 200:
            print("Browser opened successfully with random fingerprint!")
            print("Response:", response.json())
        else:
            print(f"Failed to open browser. Status code: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
open_browser_with_random_fingerprint()

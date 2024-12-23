'''Status: Successful
'''

import requests

class OpenProfile:
    def __init__(self, base_url="http://127.0.0.1:53200/api/v2/"):
        self.base_url = base_url

    def open_profile(self, profile_id, args=None, load_extensions=True, load_profile_info_page=True, cookies_backup=True, cookie=""):
        url = f"{self.base_url}profile-open"
        headers = {"Content-Type": "application/json"}
        payload = {
            "profile_id": profile_id,
            "args": args or ["--disable-extension-welcome-page"],
            "load_extensions": load_extensions,
            "load_profile_info_page": load_profile_info_page,
            "cookies_backup": cookies_backup,
            "cookie": cookie
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

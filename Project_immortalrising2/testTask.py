from ixBrowser.OpenProfile import OpenProfile

'''Status: Successful: OpenProfile'''
from ixBrowser.OpenProfile import OpenProfile  # Correct import

# Create an instance of OpenProfile
ix_browser_api = OpenProfile()

#Step1: Open a profile
profile_id = 1029  # Replace with actual profile ID
result = ix_browser_api.open_profile(profile_id=profile_id, args=["--disable-popup-blocking"])
if result:
    if result['error']['code'] == 0:
        print("Profile opened successfully!")
        print("Debugging Address:", result['data']['debugging_address'])
    else:
        print(f"Error: {result['error']['message']} (Code: {result['error']['code']})")
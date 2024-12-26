'''
Status: Successfully Run Not Test yet- --> Change Database that store Proxy table we use
Purpose: Update proxy for ixBrowser profile - by retrieving proxies from database - API, ,mySQL, mySQL WorkBench
Owner: Thuong
Date Done: 16:27pm 13.12.2024
--> Change Database that store Proxy table we use

Code Process:
Connect to Database
Retrieve active proxies from Database.
User Input for Profile Range: Get start_id and end_id from user.
Calculate Profiles end_id - start_id + 1 to set exactly number profiles = number proxies
Update proxies for each profile.
Set proxy status to "Connected" after the last profile filled.
Log any errors to errors.log.
Exit if proxy status "connected" not updated.Bcauz if not update all the profiles will use the same proxy
Call API to set profile proxy.
Exit once all updates are done.
'''
import pymysql
import requests
import json

# Kết nối cơ sở dữ liệu
def connect_database():
    try:
        connection = pymysql.connect(
            host='8.219.149.132',
            port=3306,
            user='thoungle',
            password='jfPM8d7bMc6jRasF',
            database='thoungle'
        )
        print("Kết nối cơ sở dữ liệu thành công!")
        return connection
    except pymysql.MySQLError as e:
        print("Không thể kết nối cơ sở dữ liệu:", e)
        return None

# Lấy danh sách proxy từ cơ sở dữ liệu
def fetch_proxies(number_of_proxies):
    connection = connect_database()
    if not connection:
        return []

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        try:
            # Lấy danh sách proxy có trạng thái 'Active' và giới hạn số lượng proxy cần thiết
            cursor.execute("SELECT * FROM Proxies WHERE Status = 'Active' LIMIT %s", (number_of_proxies,))
            proxies = cursor.fetchall()
            return proxies
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu proxy: {e}")
            return []
        finally:
            connection.close()

# Cập nhật trạng thái proxy
def update_proxy_status(proxy_id, status):
    valid_status = ['Active', 'Inactive', 'Connected', 'Unconnected']
    if status not in valid_status:
        print(f"Trạng thái proxy '{status}' không hợp lệ!")
        return False

    connection = connect_database()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Proxies SET Status = %s WHERE ID = %s", (status, proxy_id))
            connection.commit()
            print(f"Trạng thái của proxy {proxy_id} đã được cập nhật thành {status}")
            return True
    except Exception as e:
        print(f"Lỗi khi cập nhật trạng thái proxy {proxy_id}: {e}")
        return False
    finally:
        connection.close()


# Hàm cập nhật proxy cho từng profile
def update_proxy(profile_id, proxy_data):
    API_URL = "http://127.0.0.1:53200/api/v2/profile-update-proxy-for-custom-proxy"
    payload = {
        "profile_id": profile_id,
        "proxy_info": {
            "proxy_mode": 2,  # Chế độ custom proxy
            "proxy_check_line": "global_line",  # Dòng kiểm tra proxy
            "proxy_type": "http",  # Loại proxy
            "proxy_ip": proxy_data["proxy_ip"],
            "proxy_port": proxy_data["proxy_port"],
            "proxy_user": proxy_data.get("proxy_user", ""),
            "proxy_password": proxy_data.get("proxy_password", ""),
        },
    }

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code", -1) == 0:
                print(f"Profile {profile_id} cập nhật proxy thành công với proxy: {proxy_data['proxy_ip']}:{proxy_data['proxy_port']} với username: {proxy_data.get('proxy_user', '')}")
                return True
            else:
                raise Exception(result.get("error", {}).get("message", "Unknown error"))
        else:
            raise Exception(f"HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"Lỗi khi cập nhật proxy cho profile {profile_id}: {e}")
        return False

# Ghi log lỗi vào file
def log_error(profile_id, error_message):
    with open("errors.log", "a") as log_file:
        log_file.write(f"Profile ID: {profile_id}, Error: {error_message}\n")

# Chương trình chính
def main():
    print("Nhập khoảng Profile ID cần cập nhật proxy: ")
    start_id = int(input("Từ Profile ID: "))
    end_id = int(input("Đến Profile ID: "))

    # Tính số lượng profile cần cập nhật
    number_of_profiles_to_update = end_id - start_id + 1
    print(f"Số lượng profile cần cập nhật: {number_of_profiles_to_update}")

    print("Đang lấy danh sách proxy từ cơ sở dữ liệu...")
    proxies = fetch_proxies(number_of_profiles_to_update)

    if not proxies:
        print("Không có proxy nào cần cập nhật.")
        return

    print("Bắt đầu cập nhật proxy cho các profile...")

    for index, proxy in enumerate(proxies):
        if proxy["Status"] == "Connected":
            continue  # Bỏ qua proxy đã sử dụng

        # Tính toán profile ID sẽ cập nhật proxy
        profile_id = start_id + index
        if profile_id > end_id:
            break  # Nếu vượt qua phạm vi profile cần cập nhật thì dừng

        proxy_data = {
            "proxy_ip": proxy["IPAddress"],
            "proxy_port": proxy["Port"],
            "proxy_user": proxy.get("Username", ""),
            "proxy_password": proxy.get("Password", ""),
        }
        success = update_proxy(profile_id, proxy_data)
        if success:
            print(f"Profile {profile_id} đã cập nhật proxy thành công với proxy: {proxy_data['proxy_ip']}:{proxy_data['proxy_port']} với username: {proxy_data['proxy_user']}")
            if not update_proxy_status(proxy["ID"], "Connected"):
                print(f"Cảnh báo: Proxy {proxy['ID']} chưa được cập nhật trạng thái.")
                # Dừng chương trình nếu proxy không được cập nhật trạng thái
                print("Dừng chương trình vì proxy không được cập nhật trạng thái.")
                return
        else:
            log_error(profile_id, f"Cập nhật proxy thất bại cho profile {profile_id}")

    print("Cập nhật proxy hoàn tất!")

# Chạy chương trình chính
if __name__ == "__main__":
    main()

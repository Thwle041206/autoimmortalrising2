'''
Status: Successfully Run
Purpose: Add Gmail Account to Database
Owner: Thuong
Date Done: 18:10pm 13.12.2024

Code Process:
Note: replace the txt file to insert actual accounts

DELETE FROM Emails;
select * from thoungle.Emails;
ALTER TABLE Emails AUTO_INCREMENT = 1;
'''
import pymysql

# Kết nối cơ sở dữ liệu
def connect_database():
    connection = pymysql.connect(
        host='8.219.149.132',
        port=3306,
        user='airdrop',
        password='ncsYSAT5y3cjtfwn',
        database='airdrop'
    )
    return connection

# Hàm thêm Gmails từ file gmailAccount.txt
def insert_gmails_from_txt(txt_file):
    connection = connect_database()
    cursor = connection.cursor()

    try:
        with open(txt_file, 'r') as file:
            for line in file:
                # Xóa bỏ các khoảng trắng đầu cuối và kiểm tra nếu không phải dòng rỗng
                line = line.strip()
                if line:
                    # Tách chuỗi Gmail thành email và password
                    parts = line.split(':')
                    if len(parts) == 2:  # Kiểm tra đúng định dạng (Email:Password)
                        email = parts[0]
                        password = parts[1]

                        try:
                            # Chèn vào database
                            cursor.execute("""
                                INSERT INTO ImapEmails (EmailAddress, Password, IMAPServer, IMAPPort, Status)
                                VALUES (%s, %s, NULL, 993, 'NotUsed')
                            """, (email, password))
                        except pymysql.IntegrityError:
                            # Bỏ qua lỗi duplicate entry
                            print(f"Email đã tồn tại: {email}")

        connection.commit()
        print("Đã chèn dữ liệu Gmail vào database thành công!")
    except Exception as e:
        print(f"Lỗi trong quá trình chèn dữ liệu: {e}")
        connection.rollback()
    finally:
        connection.close()

# Gọi hàm để thêm Gmails
insert_gmails_from_txt('gmailAccount.txt')

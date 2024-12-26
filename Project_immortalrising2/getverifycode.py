import imaplib
import email
import re


def read_email_from_certik(username, password,
                           imap_server='imap.firstmail.ltd',
                           imap_port=993,
                           expected_sender='hello@passport.e.immutable.com'):
    """<hello@passport.e.immutable.com>
    'no-reply@certik.com'
    读取特定发件人的邮件内容

    :param username: 邮箱账号
    :param password: 邮箱密码
    :param imap_server: IMAP服务器地址
    :param imap_port: IMAP服务器端口
    :param expected_sender: 预期的发件人邮箱
    :return: 邮件内容或None
    """
    try:
        # 连接到IMAP服务器
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)

        # 选择收件箱
        mail.select('inbox')


        # 搜索所有邮件
        _, search_data = mail.search(None, 'ALL')

        # 获取所有邮件ID
        email_ids = search_data[0].split()

        # 从最后一封邮件开始向前搜索
        for email_id in reversed(email_ids):
            # 获取邮件
            _, email_data = mail.fetch(email_id, '(RFC822)')
            raw_email = email_data[0][1]

            # 解析邮件
            email_message = email.message_from_bytes(raw_email)

            # 检查发件人
            sender = email.utils.parseaddr(email_message['From'])[1]

            if sender == expected_sender:
                # 提取邮件内容
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                        elif part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode()
                else:
                    body = email_message.get_payload(decode=True).decode()

                # 打印邮件详细信息
                print("发件人：", sender)
                print("主题：", email_message['Subject'])
                print("发送日期：", email_message['Date'])
                print("\n邮件内容：")
                #print(body)

                # 使用正则表达式提取所有 6 位数字
                verification_code_pattern = r'(\d{6})'
                matches = re.findall(verification_code_pattern, body)

                # 检查是否找到匹配项
                if matches:
                    # 打印所有匹配的 6 位数字
                    print("所有匹配的 6 位数字：", matches)

                    # 如果匹配结果数量足够，提取第四个结果
                    if len(matches) >= 4:
                        verification_code = matches[3]  # 第四个结果是索引 3
                        print(f"提取到的验证码（第四个结果）：{verification_code}")
                    else:
                        print("匹配的 6 位数字数量不足，无法提取第四个结果")
                else:
                    print("未找到验证码")

                # 关闭连接
                mail.close()
                mail.logout()

                return body

        print("未找到符合条件的邮件")
        mail.close()
        mail.logout()
        return None

    except Exception as e:
        print(f"发生错误：{e}")
        return None


# 使用示例
if __name__ == "__main__":
    # 替换为你的实际邮箱和密码
    username = 'ovtrzpyu@esponamail.com'
    password = 'xeibdbncY4994'

    # 读取邮件
    email_content = read_email_from_certik(username, password)

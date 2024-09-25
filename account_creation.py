from email.message import EmailMessage
from random_api import random_code
from json import dump, load
import smtplib

def email_confirm_func(email):
    sender = smtplib.SMTP('smtp.gmail.com', 587)
    sender.starttls()
    sender.login("chatbox.automated@gmail.com", "ulgy wakc wfrk hwub")

    message = EmailMessage()
    message["From"] = "chatbox.automated@gmail.com"
    message["To"] = email
    message["Subject"] = "Confirm chatbox email"

    code = random_code()

    message.set_content(f"Your code is: {code}")

    sender.send_message(message)
    sender.quit()

    with open("account-storage/email-confirm.json", "r+") as file:
        data = load(file)
        data["codes"][email] = code

        file.seek(0)
        file.truncate()
        dump(data, file, indent=4)

def confirm_code_func(data):
    email = data.get("email")
    code = data.get("code")

    with open("account-storage/email-confirm.json", "r") as file:
        data = load(file)

        if int(data["codes"][email]) == int(code):
            print("Correct code")
        else:
            print(code)
            print(data["codes"][email])

    return ""
from email.message import EmailMessage
from random_api import random_code
from json import dump, load
from flask import session
import smtplib

def check_for_email_func(email, socket):
    with open("account-storage/accounts.json", "r") as file:
        data = load(file)

        for v in data["accounts"]:
            if v.get("email").upper() == email.upper():
                socket.emit("email-used")
                return ""
        
        socket.emit("email-free")

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
    
    session["email"] = email

def confirm_code_func(data, socket):
    email = session["email"]
    code = data.get("code")

    with open("account-storage/email-confirm.json", "r") as file:
        data = load(file)

        if str(data["codes"][email]).replace(" ", "") == str(code).replace(" ", ""):
            socket.emit("correct code")
        else:
            socket.emit("incorrect code")

    return ""

def check_for_username_func(username, socket):
    with open("account-storage/accounts.json", "r") as file:
        data = load(file)

        for v in data["accounts"]:
            if v.get("username").upper() == username.upper():
                socket.emit("username-used")
                return ""
        
        socket.emit("username-free")


def create_account_func(data):
    username = data.get("username")
    password = data.get("password")
    email = session["email"]
    
    with open("account-storage/accounts.json", "r+") as file:
        accounts = load(file)
        accounts["accounts"].append({"username": username, "email": email, "password": password})

        file.seek(0)
        file.truncate()
        dump(accounts, file, indent=4)
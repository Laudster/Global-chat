from json import load
from flask import session

def login_attempt_func(data, socket):
    email = data.get("email")
    password = data.get("password")

    with open("account-storage/accounts.json", "r") as file:
        data = load(file)

        for v in data["accounts"]:
            if v.get("email") == email:
                if v.get("password") == password:
                    socket.emit("login-sucess", v.get("username"))
                    session["login"] = v.get("username")
                    return ""
        
        socket.emit("login-fail")

def get_username_func():
    if "login" in session:
        return session["login"]
    else:
        return "Anon"
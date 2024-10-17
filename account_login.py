from json import load
from flask import request, session

def login_attempt_func(data, socket):
    email = data.get("email")
    password = data.get("password")

    with open("account-storage/accounts.json", "r") as file:
        data = load(file)

        for v in data["accounts"]:
            if v.get("email") == email:
                if v.get("password") == password:
                    socket.emit("login-sucess", v.get("username"), to=request.sid)
                    session.permanent = True
                    session["login"] = v.get("username")
                    return ""
        
        socket.emit("login-fail", to=request.sid)

def get_username_func():
    print(session)
    return session.get("login", "Anon")
from json import load
from flask import request, session, jsonify

def login_attempt_func():
    data = request.get_json()
    print(data)
    email = data["email"]
    password = data["password"]

    print(email)
    print(password)

    with open("account-storage/accounts.json", "r") as file:
        savedata = load(file)

        for v in savedata["accounts"]:
            if v.get("email") == email:
                if v.get("password") == password:
                    session["login"] = v.get("username")
                    session.permanent = True
                    print(session)
                    return jsonify({"status": "login-sucess", "username": v.get("username")})
        
        return jsonify({"stauts": "login-fail"})

def get_username_func():
    return session.get("login", "Anon")
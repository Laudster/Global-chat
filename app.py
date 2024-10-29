from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from os import path, getenv
from json import load
from account_creation import check_for_email_func, email_confirm_func, confirm_code_func, check_for_username_func, create_account_func
from account_login import login_attempt_func, get_username_func
from get_endpoints import get_messages_endpoint, get_image_endpoint
from post_endpoints import new_image_endpoint, post_endpoint
from room_endpoints import new_room_endpoint, delete_room_endpoint, get_rooms_endpoint, init_list_endpoint, remove_list_endpoint, get_list_statuses_endpoint
from dotenv import load_dotenv
from datetime import timedelta

app = Flask(__name__)
socket = SocketIO(app, max_http_buffer_size=500000000, manage_session=False) #5mb

load_dotenv()
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

@socket.on("establish_relation")
def on_join(data):
    if data.get("room") == "/":
        join_room("/Global")
        print("connection established with user on /Global")
    else:
        join_room(data.get("room"))
        print("connection established with user on " + data.get("room"))

@app.route("/login-attempt", methods=["POST"])
def login_attempt(): return login_attempt_func()

@socket.on("get-username")
def get_username(): return get_username_func()

@socket.on("check-for-email")
def check_for_email(email): check_for_email_func(email, socket)

@socket.on("email-confirm")
def email_confirm(email): email_confirm_func(email)

@socket.on("email-code")
def confirm_code(data): confirm_code_func(data, socket)

@socket.on("username-check")
def check_for_username(data): check_for_username_func(data, socket)

@socket.on("account-create")
def account_create(data): create_account_func(data)

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")
    with open(f"boards/Global.json", "r") as file:
        data = load(file)
        messages = data["messages"]
    return render_template("chat.html", messages=messages, displayer=display_name, title="Global")

@app.route("/<room>")
def room(room):
    if path.exists(f"boards/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")
        with open(f"boards/{room}.json", "r") as file:
            data = load(file)
            messages = data["messages"]

        return render_template("chat.html", messages=messages, displayer=display_name, title=room)
    return redirect(url_for("globall"))

@app.route("/get-image", methods=["GET"])
def get_image(): return get_image_endpoint()

@socket.on("get-messages")
def get_messages(data): return get_messages_endpoint(data)

@socket.on("get-rooms")
def get_rooms(): return get_rooms_endpoint()

@socket.on("new-message")
def post(data): return post_endpoint(data, socket)

@socket.on("new-image")
def new_image(image): return new_image_endpoint(image)

@socket.on("new-room")
def new_room(data): return new_room_endpoint(data)

@socket.on("delete-room")
def delete_room(data): return delete_room_endpoint(data)

@socket.on("init-list")
def init_list(data): return init_list_endpoint(data)

@socket.on("remove-list")
def remove_list(data): return remove_list_endpoint(data)

@socket.on("get-list-statuses")
def get_list_statuses(data): return get_list_statuses_endpoint(data)

if __name__ == "__main__":
    #socket.run(app, debug=False, allow_unsafe_werkzeug, host="0.0.0.0") # public
    socket.run(app, debug=True, allow_unsafe_werkzeug=True) # dev
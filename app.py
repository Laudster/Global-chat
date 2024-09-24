from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from get_endpoints import get_messages_endpoint, get_image_endpoint, get_rooms_endpoint
from post_endpoints import new_room_endpoint, new_image_endpoint, post_endpoint
from email.message import EmailMessage
import smtplib
import json
import os

app = Flask(__name__)
socket = SocketIO(app, max_http_buffer_size=500000000) #5mb

@socket.on("establish_relation")
def on_join(data):
    if data.get("room") == "/":
        join_room("/Global")
        print("connection established with /Global")
    else:
        join_room(data.get("room"))
        print("connection established with " + data.get("room"))

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")

    with open(f"boards/Global.json", "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("chat.html", messages=messages, displayer=display_name, title="Global")

@socket.on("email-confirm")
def email_confirm(email):
    sender = smtplib.SMTP('smtp.gmail.com', 587)
    sender.starttls()
    sender.login("chatbox.automated@gmail.com", "ulgy wakc wfrk hwub")
    message = EmailMessage()
    message["From"] = "chatbox.automated@gmail.com"
    message["To"] = email
    message["Subject"] = "Confirm chatbox email"
    message.set_content("Your code is: ")
    sender.send_message(message)
    sender.quit()

@app.route("/<room>")
def room(room):
    if os.path.exists(f"boards/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")
        with open(f"boards/{room}.json", "r") as file:
            data = json.load(file)
            messages = data["messages"]


        return render_template("chat.html", messages=messages, displayer=display_name, title=room)
    return redirect(url_for("globall"))

@app.route("/get-image", methods=["GET"])
def get_image():
    return get_image_endpoint()

@socket.on("get-messages")
def get_messages(data):
    return get_messages_endpoint(data)

@socket.on("get-rooms")
def get_rooms():
    return get_rooms_endpoint()

@socket.on("new-message")
def post(data):
    return post_endpoint(data, socket)

@socket.on("new-image")
def new_image(image):
    return new_image_endpoint(image)

@socket.on("new-room")
def new_room(data):
    return new_room_endpoint(data)

if __name__ == "__main__":
    #socket.run(app, debug=False, host="0.0.0.0") # public
    socket.run(app, debug=True)
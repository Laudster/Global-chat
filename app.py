from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from get_endpoints import *
from post_endpoints import new_room_endpoint, new_image_endpoint, post_endpoint

app = Flask(__name__)
#app.config["SECRET_KEY"] = "hemmelig"
socket = SocketIO(app, max_http_buffer_size=500000000) #5mb


@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")\

    with open(f"{boards}/Global.json", "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("chat.html", messages=messages, displayer=display_name, title="Global")

@app.route("/<room>")
def room(room):
    if os.path.exists(f"{boards}/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")

        with open(f"{boards}/{room}.json", "r") as file:
            data = json.load(file)
            messages = data["messages"]

        return render_template("chat.html", messages=messages, displayer=display_name, title=room)
    
    return redirect(url_for("globall"))

@app.route("/get-situation")
def situation_report():
    return situation_report_endpoint()

@app.route("/get-messages", methods=["GET"])
def get_messages():
    return get_messages_endpoint()

@app.route("/get-image", methods=["GET"])
def get_image():
    return get_image_endpoint()

@app.route("/get-rooms", methods=["GET"])
def get_rooms():
    return get_rooms_endpoint()

@socket.on("new-message")
def post(data):
    return post_endpoint(data, socket)

@socket.on("new-image")
def new_image(image):
    return new_image_endpoint(image)

@app.route("/new-room", methods=["POST"])
def new_room():
    return new_room_endpoint()

if __name__ == "__main__":
    #socket.run(app, debug=False, host="0.0.0.0") # public
    socket.run(app, debug=True)
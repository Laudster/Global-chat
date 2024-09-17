from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from post_endpoints import *
from get_endpoints import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "hemmelig"
SocketIO = SocketIO(app)

@SocketIO.on("websocket_event")
def message(data):
    print(data["data"])

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

@app.route("/new-message", methods=["POST"])
def post():
    return post_endpoint()

@app.route("/new-room", methods=["POST"])
def new_room():
    return new_room_endpoint()

if __name__ == "__main__":
    #SocketIO.run(app, debug=False, host="0.0.0.0") # public
    SocketIO.run(app, debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

def update_file(file, data):
    file.seek(0)
    file.truncate()
    json.dump(data, file, indent=4)

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")\

    with open("saves/Global.json", "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("global.html", messages=messages, displayer=display_name)

@app.route("/<room>")
def room(room):
    if os.path.exists(f"saves/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")

        with open(f"saves/{room}.json", "r") as file:
            data = json.load(file)
            messages = data["messages"]

        return render_template("global.html", messages=messages, displayer=display_name)
    
    return redirect(url_for("globall", display_name=request.args.get("display_name")))


@app.route("/get-messages", methods=["GET"])
def get_messages():
    room = request.args.get("room")

    room = room[1:len(room)]

    if room == "/" or room == "":
        room = "global"
    elif os.path.exists(f"saves/{room}.json") == True:
        messages : str

        with open(f"saves/{room}.json", "r") as file:
            message_data = json.load(file)

        return jsonify(message_data)

    with open(f"saves/{room}.json", "r") as file:
        message_data = json.load(file)

    return jsonify(message_data)

@app.route("/get-rooms", methods=["GET"])
def get_rooms():
    data = [os.path.join("saves", f) for f in os.listdir("saves") if os.path.isfile(os.path.join("saves", f))]
    data = sorted(data, key=lambda x: os.path.getctime(x))

    for i, v in enumerate(data):
        split = v.split("\\")
        data[i] = split[len(split) - 1]
    
    for i, v in enumerate(data):
        split = v.split(".")
        data[i] = split[0]

    data.remove("Global")
    
    return data

@app.route("/new-message", methods=["POST"])
def post():
    message = request.form.get("message")
    display_name = request.form.get("display_name")

    room = request.form.get("room")
    room = room[1:len(room)]

    if room == "" or room == "/":
        room = "Global"

    with open(f"saves/{room}.json", "r+") as file:
        message_data = json.load(file)
        if not display_name:
            display_name = "User"
        message_data["messages"].append({"value": message, "displayname": display_name+": "})
        update_file(file, message_data)

    return jsonify()

@app.route("/new-room", methods=["POST"])
def new_room():
    room_name = request.form.get("room_name")

    if not os.path.exists("saves/" + room_name + ".json"):
        with open("saves/" + room_name + ".json", "w") as file:
            data = {"messages": []}
            json.dump(data, file, indent=4)
    
    return jsonify()


if __name__ == "__main__":
    #app.run(debug=False, host="0.0.0.0") public
    app.run(debug=True) # debug